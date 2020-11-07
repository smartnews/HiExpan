"""
__author__: Jiaming Shen, Ellen Wu
__description__: Generate entity list from sentence.json.raw and output sentence.json
    Input: 1) the sentence.json.raw
    Output: 1) entity2id.txt, 2) entity2surface_names.txt, 3) entity2freq.txt, and 4) sentence.json
"""
import json
from collections import defaultdict
import sys
import mmap
from tqdm import tqdm


def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def deduplicate(ems):
    """Remove duplicates in entity mention list

    ems: a dictionary
    return: a dictionary without duplicates 
    """
    uniques = set([])
    for em in ems:
        if 'type' in em:
            uniques.add((em['entityId'], em['start'], em['end'], em['text'], em['type'])) 
    
    res = []
    for ele in uniques:
        res.append({'entityId': ele[0], 'start': ele[1], 'end': ele[2], 'text': ele[3], 'type': ele[4]})
    return res


def main(corpusName):
    inputFile = '../../data/'+corpusName+'/intermediate/segmentation-one.json'

    outputEntity2IDFile = '../../data/' + corpusName + '/intermediate/entity2id_one.txt'
    outputEntity2SurfaceNameFile = '../../data/' + corpusName + '/intermediate/entity2surface_names_one.txt'
    outputEntity2FreqFile = '../../data/' + corpusName + '/intermediate/entity2freq_one.txt'
    
    cnt = 0
    entity2id = {}
    entity2surface_names = {}
    entity2freq = defaultdict(int)

    with open(inputFile, "r") as fin:
        for line in tqdm(fin, total=get_num_lines(inputFile), desc="Extract Key Terms from Corpus"):
            line = line.strip()
            try:
                sentence = json.loads(line)
            except ValueError:
                continue
            lemma_list = sentence["lemma"]
            for mention in sentence["entityMentions"]:
                entity = mention["text"].lower()
                if entity == "":  # this can happen because AutoPhrase returns <phrase></phrase>
                    continue
                lemma_signature = "_".join(lemma_list[mention["start"]:mention["end"]+1])

                if lemma_signature not in entity2id:  # a new "entity"
                    entity2id[lemma_signature] = cnt
                    cnt += 1
                    entity2surface_names[lemma_signature] = defaultdict(int)

                entity2freq[lemma_signature] += 1
                entity2surface_names[lemma_signature][entity] += 1

    
    with open(outputEntity2IDFile, "w") as fout:
        for ele in sorted(entity2id.items(), key = lambda x:(x[0], x[1])):
            fout.write("{}\t{}\n".format(ele[0], ele[1]))

    with open(outputEntity2SurfaceNameFile, "w") as fout:
        for ele in sorted(entity2surface_names.items(), key = lambda x:x[0]):
            fout.write("{}\t{}\n".format(ele[0], str(dict(ele[1]))))

    with open(outputEntity2FreqFile, "w") as fout:
        for ele in sorted(entity2freq.items(), key=lambda x: x[0]):
            fout.write("{}\t{}\n".format(ele[0], ele[1]))


if __name__ == '__main__':
    corpusName = sys.argv[1]
    main(corpusName)
