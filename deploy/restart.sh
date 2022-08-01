#!/bin/bash
cd /home/www/code/quranbot-admin

git pull
git reset --hard origin/master

/home/www/.poetry/bin/poetry install --no-dev

sudo supervisorctl reread
sudo supervisorctl update

sudo supervisorctl restart quranbot-admin
