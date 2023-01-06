#!/bin/sh

rm -rf ./venv
virtualenv ./venv
. ./venv/bin/activate
pip install -r ./requirements.txt
cd ./streetscrape/
sh ./run_swingtradebot.sh
sh ./run_thestreet.sh && sh ./run_zacks.sh && sh ./run_gurufocus.sh