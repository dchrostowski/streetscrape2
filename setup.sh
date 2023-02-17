#!/bin/sh

rm -rf ./venv
virtualenv ./venv
. ./venv/bin/activate
pip install -r ./requirements.txt
sudo apt-get install -y libgbm-dev libasound2 daemon nodejs
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 16
nvm use 16
cd ./streetscrape/headless_browsing
npm install
