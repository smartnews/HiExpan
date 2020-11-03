#!/bin/bash
path=$(pwd)
data_path="../../data/sample_dataset/intermediate"
corpus_name="sample_dataset"
ONE_FILE="-one"
if [ -z $1 ] ; then
    echo -e "Please specify input file_name"
    exit 1
fi

num_thread=20
MIN_SUP=10
multi=0.75
single=0.65

# ----Run This Before Setting Autophrase Threshold-----
# python extractCorpus.py ${data_path} ${num_thread} #convert sentence.json to sentence.txt

# # ----Run This After Setting Autophrase Threshold-----
# cd ../tools/AutoPhrase/
# bash phrasal_segmentation.sh ${corpus_name} ../${data_path}/$1 ${multi} ${single} $num_thread ${ONE_FILE}
# mv models/${corpus_name}/segmentation-one.txt ${path}/${data_path}/
# cd ${path}

### Generating Output for Phrasified data_path ###
python process_segmentation.py --multi ${multi} --single ${single} --output ${data_path} --mode phrase

#mv ${data_path}/phrase_dataset_${multi}_${single}.txt ${data_path}/phrase_text.txt
#python extractSegmentation.py ${data_path}
#python extractBertEmbedding.py ${data_path} 20
