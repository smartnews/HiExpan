FROM rappdw/docker-java-python:zulu1.8.0_262-python3.7.9
MAINTAINER Meng Lee <meng.lee@smartnews.com>

RUN \
    echo "===> install g++" && \
    apt-get update && apt-get install -y --force-yes g++

RUN \
    echo "===> install make, curl, perl" && \
    apt-get update && apt-get install -y --force-yes make curl perl

WORKDIR /data/app/
ENV ROOT_DIR /data/app
COPY pke_requirements.txt ./
COPY pke ./pke
COPY src/tools/AutoPhrase ./src/tools/AutoPhrase
COPY src/pke ./src/pke
COPY src/server ./src/server


RUN \
    echo "===> compile AutoPhrase..." && \
    cd $ROOT_DIR/src/tools/AutoPhrase && bash compile.sh 
    
ENV COMPILE 0

RUN \
    echo "===> clean up..."  && \
    apt-get purge -y --force-yes make && \
    apt-get autoremove -y --purge make && \
    rm -rf /var/cache/oracle-jdk8-installer  && \
    apt-get clean  && \
    rm -rf /var/lib/apt/lists/*
    
RUN \
    echo "===> install python dependencies..." && \
    cd $ROOT_DIR && pip install -r pke_requirements.txt && \
    cd $ROOT_DIR/pke && pip install -e . && \
    python -m nltk.downloader stopwords && \
    python -m nltk.downloader universal_tagset && \
    python -m spacy download en

RUN mkdir -p $ROOT_DIR/server/logs

WORKDIR /data/app/src/server/

ENTRYPOINT ["python", "server.py"]



# COPY src/pke ./src/pke
# ENV input_document=/data/app/src/pke/test.txt
# RUN cd $ROOT_DIR/src/pke && sh pke_one_doc.sh sn ${input_document}