#!/bin/sh
gunicorn --worker-class eventlet -w 4 -b 0.0.0.0:8000 run:app