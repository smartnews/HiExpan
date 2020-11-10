#!/bin/bash
path=$(pwd)
corpus_name=$1
ONE_FILE="-one"
if [ -z $2 ] ; then
	echo -e "Please specify input file_name and corpus_name (e.g. sn)"
    exit 1
fi

num_thread=20
MIN_SUP=10
multi=0.6
single=0.9

cd ../tools/AutoPhrase/
bash phrasal_segmentation_pke.sh ${corpus_name} $2 ${multi} ${single} $num_thread
cd ${path}

python test_input_article.py $2-seg.txt
