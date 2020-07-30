#!/bin/bash

cd /var/src/app

if [ ! -d var/db ]; then
  echo "Creating database directory."
  mkdir var/db
fi
if [ ! -f var/db/db.sqlite3 ]; then
  echo "No database found, initializing..."
  make init
fi

python $@
