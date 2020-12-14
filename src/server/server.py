#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
main class for server
'''

import logging
import logging.config
import os
import json

from cloghandler import ConcurrentRotatingFileHandler
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.web


#import conf.conf as conf
from conf.logging_config import logging_conf
from handlers.serve_handler import ServeHandler

define("segmentation_model", default="sn", 
       help="pretrained segmentation model", type=str)
define("num_process", default=1, 
       help="number of concurrent processes", type=int)
define("port", default=8901, 
       help="run on the given port", type=int)


logging.config.dictConfig(logging_conf)


class HealthCheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("OK")


class Application(tornado.web.Application):
    '''main class'''
    

    def __init__(self, segmentation_model):
        handlers = [
            (r'/ping', HealthCheckHandler),
            (r'/serve', ServeHandler),
            (r'/', ServeHandler),
        ]

        self.segmentation_model = segmentation_model 
        
        # create temporary data dir
        self.data_dir = data_dir = '/tmp'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        tornado.web.Application.__init__(self, handlers, debug=True)

        logging.info('process starts: ' + str(os.getpid()))


def main():
    '''main func'''
    tornado.options.parse_command_line()
    port = int(options.port)
    num_process = int(options.num_process)

    if num_process < 2:
        server = tornado.httpserver.HTTPServer(Application(
            options.segmentation_model), xheaders=True)
        server.listen(port)
    else:
        sockets = tornado.netutil.bind_sockets(port)
        tornado.process.fork_processes(num_process)
        server = tornado.httpserver.HTTPServer(Application(
            options.segmentation_model), xheaders=True, decompress_request=True)
        server.add_sockets(sockets)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
