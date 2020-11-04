#!/bin/bash
path=$(pwd)
corpus_name=$1
data_path="../../data/${corpus_name}/intermediate"
ONE_FILE="-one"
if [ -z $2 ] ; then
	echo -e "Please specify input file_name and corpus_name (e.g. sn)"
    exit 1
fi

num_thread=20
MIN_SUP=10
multi=0.75
single=0.65

cd ../tools/AutoPhrase/
bash phrasal_segmentation.sh ${corpus_name} ../${data_path}/$2 ${multi} ${single} $num_thread ${ONE_FILE}
mv models/${corpus_name}/segmentation-one.txt ${path}/${data_path}/
cd ${path}

### Generating Output for Phrasified data_path ###
python process_segmentation.py --multi ${multi} --single ${single} --output ${data_path} --mode phrase

