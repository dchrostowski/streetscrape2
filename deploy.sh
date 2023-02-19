#!/bin/sh
CWD=$(pwd)
. ./venv/bin/activate
killall scrapyd
daemon --chdir=$CWD/streetscrape/ scrapyd
cd ./streetscrape/
scrapyd-deploy production


