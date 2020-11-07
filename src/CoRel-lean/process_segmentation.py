import argparse
import math
import ast
import json
from spacy.lang.en.stop_words import STOP_WORDS
#import spacy

DEFAULT_PHRASE_SCORE = 0.8
DEFAULT_SCORE_IN_DOC_FOR_STOP_WORDS = -9999

if __name__=="__main__":
	CORPUS_SIZE = 27.0

	parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--multi', default='0.8')
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
	
	phrase_freq_in_doc = {}  #load TF from the input document
	with open(args.input_path+'/entity2surface_names_one.txt') as f:
		for line in f:
			line = line.strip()
			if(line.split('\t')[0] != '-PRON-'):
				entity_DF = ast.literal_eval(line.split('\t')[1])
				key = list(entity_DF.keys())[0]
				#group the counts of similar forms of the same entity into one
				total_count = sum(entity_DF.values())
				if(list(entity_DF.keys())[0] in phrase_freq_in_doc):
					phrase_freq_in_doc[key] += total_count
				else:
					phrase_freq_in_doc.update({key: total_count}) 

	phrase_DF = {} #load document frequency from corpus
	with open(args.input_path+'/entity2surface_names.txt') as f:
		for line in f:
			line = line.strip()
			if(line.split('\t')[0] != '-PRON-'):
				entity_DF = ast.literal_eval(line.split('\t')[1])
				key = list(entity_DF.keys())[0]
				#group the counts of similar forms of the same entity into one
				total_count = sum(entity_DF.values())
				if(list(entity_DF.keys())[0] in phrase_DF):
					phrase_DF[key] += total_count
				else:
					phrase_DF.update({key: total_count}) 
	
	# Load English tokenizer, tagger, parser, NER and word vectors
	#nlp = spacy.load('en_core_web_lg')

	phrase_score_in_doc = {} #for each new doc, set the phrase_score_in_doc to zero
	word_score_in_doc = {}
	for key_phrase, freq_in_doc in phrase_freq_in_doc.items():
		if key_phrase not in phrase_score:
			phrase_score[key_phrase] = DEFAULT_PHRASE_SCORE
			print("Entity: {} was not found in AutoPhrase.txt\n".format(key_phrase))
		if key_phrase in phrase_DF:
			df = phrase_DF[key_phrase]				
		else:
			#print("Entity: {} was not found in phrase_DF.txt\n".format(key_phrase))
			continue
		if(key_phrase in STOP_WORDS):
			score = DEFAULT_SCORE_IN_DOC_FOR_STOP_WORDS
		else:	
			score = freq_in_doc *  CORPUS_SIZE/(df+1) * math.sqrt(phrase_score[key_phrase]) #this operation can be vectorize to accelerate
		phrase_score_in_doc[key_phrase] = {"score": score, "tf": freq_in_doc, "DF": df, "phrase_score": phrase_score[key_phrase] }
			
	#sort by score
	sorted_phrase_score = {k: v for k, v in sorted(phrase_score_in_doc.items(), key=lambda item: item[1]["score"], reverse=True)}
	#print(json.dumps(sorted_phrase_score, indent=1)) 
	with open(file_name, 'w') as g:
		g.write(json.dumps(sorted_phrase_score, indent=1))
