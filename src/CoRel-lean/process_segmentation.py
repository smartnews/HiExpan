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
	parser.add_argument('--input_path',default='20news')
	args = parser.parse_args()
	file_name = args.input_path+'/phrase_dataset_'+str(args.multi)+'_'+str(args.single)+'.txt'
	phrase_score = {}
	phrase_IDF = {}

	with open(args.input_path+'/AutoPhrase.txt') as f:
		for line in f:
			line = line.strip()
			cur_phrase_score = line.split('\t')
			phrase_score[cur_phrase_score[1]] = float(cur_phrase_score[0]) 	
	
	phrase_DF = {}
	with open(args.input_path+'/entity2surface_names.txt') as f:
		for line in f:
			line = line.strip()
			if(line.split('\t')[0] != '-PRON-'):
				entity_DF = ast.literal_eval(line.split('\t')[1])
				#group the counts of similar forms of the same entity into one
				total_count = sum(entity_DF.values())
				key = list(entity_DF.keys())[0]
				phrase_DF.update({key: total_count}) #IDF
	
	phrase_freq_in_doc = {} 
	with open(args.input_path+'/entity2surface_names_one.txt') as f:
		for line in f:
			line = line.strip()
			if(line.split('\t')[0] != '-PRON-'):
				key_phrase = ast.literal_eval(line.split('\t')[1])
				total_count = sum(key_phrase.values())
				key = list(key_phrase.keys())[0]
				phrase_freq_in_doc.update({key: total_count})
			
	phrase_score_in_doc = {} #for each new doc, set the phrase_score_in_doc to zero
	for freq_in_doc, key_phrase in enumerate(phrase_freq_in_doc):
		if key_phrase in phrase_score:
			if key_phrase in phrase_DF:
				df = phrase_DF[key_phrase]				
			else:
				df = 0
			phrase_score_in_doc[key_phrase] = freq_in_doc *  (CORPUS_SIZE/(df+1)) * math.sqrt(phrase_score[key_phrase]) #this operation can be vectorize to accelerate
		else:
			print("Entity: {} was not found in AutoPhrase.txt\n".format(key_phrase))
	#sort by score
	sorted_phrase_score = {k: v for k, v in sorted(phrase_score_in_doc.items(), key=lambda item: item[1], reverse=True)}
	print(json.dumps(sorted_phrase_score, indent=1)) 
	with open(file_name, 'w') as g:
		g.write(json.dumps(sorted_phrase_score, indent=1))
