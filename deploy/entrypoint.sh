#!/bin/bash

cd /code || exit
echo "Starting yadisk_api service:"
echo '#1 migrating database...'
wait-for-it postgres:5432 -- alembic upgrade head
echo '#2 starting backend...'
gunicorn src.yadisk_api.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000