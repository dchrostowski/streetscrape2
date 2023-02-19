#!/bin/sh

#!/bin/sh
CWD=$(pwd)
. ./venv/bin/activate
cd $CWD/streetscrape/
python api_scheduler.py
python ingest_gurufocus.py
