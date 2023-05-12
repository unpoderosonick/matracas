#!/usr/bin/env bash
# exit on error
set -o errexit

python cesem/manage.py collectstatic --no-input
python cesem/manage.py migrate