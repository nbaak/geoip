#!/bin/bash

docker rmi geoip
docker build -t geoip .
