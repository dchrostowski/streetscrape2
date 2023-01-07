#!/bin/sh

rm -rf ./venv
virtualenv ./venv
. ./venv/bin/activate
pip install -r ./requirements.txt
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
. ~/.profile
nvm install 16
nvm use 16
cd ./streetscrape/puppeteer
npm install
sudo apt-get install -y libgbm-dev libasound2
