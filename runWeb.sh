#!/bin/sh
# gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 run:app
source linuxvenv/bin/activate
python run.py