#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))
echo $IP2LOCATION_TOKEN > ${THIS_DIR}/auth.token

/etc/init.d/cron start & 

python3 ${THIS_DIR}/App.py
