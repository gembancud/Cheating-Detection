#!/bin/sh
gunicorn --worker-class eventlet -w 2 -b 0.0.0.0:5000 run:app