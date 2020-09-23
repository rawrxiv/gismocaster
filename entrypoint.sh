#!/bin/bash

cd /usr/src/app

if [ ! -d var/db ]; then
  echo "Creating database directory."
  mkdir var/db
fi
if [ ! -f var/db/db.sqlite3 ]; then
  echo "No database found, initializing..."
  make init
fi

python ./web/manage.py runserver 0.0.0.0:${PORT} --noreload $@

