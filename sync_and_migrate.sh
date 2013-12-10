#!/bin/bash

python manage.py syncdb
source migrate_db.sh
