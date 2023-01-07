#!/bin/sh

. ./venv/bin/activate
cd ./streetscrape/
sh ./run_swingtradebot.sh
sh ./run_gurufocus.sh
cd puppeteer/
nvm install 16
nvm use 16
node ./gurufocus.js
cd ../
python ingest_gurufocus.py
sh ./run_thestreet.sh && sh ./run_zacks.sh