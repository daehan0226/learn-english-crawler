#!/bin/bash
cd /home/ubuntu/learn-english-app/learn-english-crawler
source /home/ubuntu/learn-english-app/learn-english-crawler/venv/bin/activate
python ./main.py keyword=$1 keyword_type=$2 env=$3
