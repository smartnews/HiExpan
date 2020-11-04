import argparse
import math
import ast
import json

if __name__=="__main__":
	CORPUS_SIZE = 27.0

	parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--multi', default='0.5')
	parser.add_argument('--single', default = '0.8')
	parser.add_argument('--mode', default='whole', choices=['phrase', 'whole'])
	parser.add_argument('--output',default='20news')
	args = parser.parse_args()
	file_name = args.output+'/phrase_dataset_'+str(args.multi)+'_'+str(args.single)+'.txt'
	phrase_score = {}
	phrase_IDF = {}

	with open(args.output+'/AutoPhrase.txt') as f:
		for line in f:
			if len(line.strip().split('\t'))<2:
				print(line)
			phrase_score[line.strip().split('\t')[1]] = float(line.split('\t')[0]) #Autophrase score. Eric [TODO] Need to add special handling for corner case like the phrase "tcp / ip" in entity2surface_names, the AutoPhrase file says "tcp ip", while  
	with open(args.output+'/entity2surface_names.txt') as f:
		for line in f:
			if len(line.strip().split('\t'))<2:
				print(line)
			phrase_IDF[line.strip().split('\t')[0]] = ast.literal_eval(line.split('\t')[1]) #IDF
	
	phrase_freq_in_doc = {} 
	with open(args.output+'/segmentation-one.txt') as f:
		with open(file_name, 'w') as g:
			num_lines = 0
			word_count = 0
			for line in f:
				num_lines += 1
				temp = line.split('<phrase>')
				for seg in temp:
					temp2 = seg.split('</phrase>')
					if len(temp2) > 1:
						phrase_text = ('_').join(temp2[0].split(' '))
						if(phrase_text in phrase_freq_in_doc):
							phrase_freq_in_doc[phrase_text] += 1
						else:
							phrase_freq_in_doc[phrase_text] = 0
					word_count += 1
	
	phrase_score_in_doc = {} #for each new doc, set the phrase_score_in_doc to zero
	for freq_in_doc, key_phrase in enumerate(phrase_freq_in_doc):
		if key_phrase in phrase_IDF:
			for df, entity in enumerate(phrase_IDF[key_phrase]):  #although there is only one nested dictionary for each key_phrase, I am still using enumerate. There may be a better way of directly access the first item in the nested dictionary 
				if entity in phrase_score:
					phrase_score_in_doc[entity] = freq_in_doc *  (CORPUS_SIZE/(df+1)) * phrase_score[entity] #this operation can be vectorize to accelerate
				else:
					print("Entity: {} was not found in AutoPhrase.txt\n".format(entity))
	#sort by score
	sorted_phrase_score = {k: v for k, v in sorted(phrase_score_in_doc.items(), key=lambda item: item[1], reverse=True)}
	print(json.dumps(sorted_phrase_score, indent=1))
