#!/usr/bin/env python

import os
import pke
import json
import time
import logging
import traceback
import subprocess
import tornado.gen
import tornado.web


class ServeHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, *args, **kwargs):
        super(ServeHandler, self).__init__(application, request)
        self.uid = time.time()


    @tornado.gen.coroutine
    @tornado.web.asynchronous
    async def post(self):
        self.uid = 'unavailable'
        start_time = time.time()
        
        try:
            # parse request 
            req = json.loads(self.request.body)
            logging.info('receive: %s', req)
            self.uid = link_id = req['link_id']
            title, content = req['title'], req['content']


            # build raw text
            raw_text = ' '.join((title, content)) + '\n'

            # save raw text as file for processing
            req_fname = f'{link_id}_{start_time}.txt'
            req_fname = os.path.join(self.application.data_dir, req_fname)
            with open(req_fname, 'w') as fp:
                fp.write(raw_text)

            # segmentation by invoking shell script
            subprocess.call([
                'sh', 
                os.path.join(os.getcwd(), '../pke/pke_one_doc.sh'),
                self.application.segmentation_model,
                req_fname,
                'ignore_test_input_article.py'
            ])

            # pke from segmented file
            segmented_fname = req_fname + '-seg.txt'
            extractor = pke.unsupervised.TopicRank()
            extractor.load_document(segmented_fname, language='en')
            extractor.candidate_selection()
            extractor.candidate_weighting()
            kp_scores = extractor.get_n_best(n=20)

            # build response
            result = dict(status=0, debug={})
            keyphrases = []
            for kp, score in kp_scores:
                keyphrases.append(kp)

            result['keyphrases'] = keyphrases
        
        except Exception as e:
            e_name = e.__class__.__name__
            if e_name in ['KeyError', 'AssertionError']:
                self.set_status(400)
            else:
                self.set_status(500)
            
            detail_err = traceback.format_exc()            
            req = self.request.body if req is None else req
            logging.error('uid: %s | error: %s | req: %s ', self.uid, detail_err, req)
            result['debug']['err'] = 'err: %s' % detail_err
            result['status'] = 1
            
        finally:
            timecost = time.time() - start_time

            result['debug']['uid'] = self.uid
            result['debug']['timecost'] = timecost
            result = json.dumps(result, ensure_ascii=False)
            self.finish(result)
            
            # cleanup temp files
            for f in [req_fname, segmented_fname]:
                if os.path.exists(f):
                    os.remove(f)
