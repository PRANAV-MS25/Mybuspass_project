#!/usr/bin/env bash
# Render runs this script every time you deploy

set -o errexit   # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data
