#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))
echo $IP2LOCATION_TOKEN > /geoip/auth.token

/etc/init.d/cron start & 

python3 ${THIS_DIR}/App.py
