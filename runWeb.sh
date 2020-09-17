#!/bin/sh
source linuxvenv/bin/activate
# gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 run:app
python run.py