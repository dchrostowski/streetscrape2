#!/bin/sh


export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
CWD=$(pwd)
. ./venv/bin/activate
[ ! -f "$CWD/streetscrape/twistd.pid"] && sh ./deploy.sh

cd $CWD/streetscrape/
nvm use 16
python api_scheduler.py

