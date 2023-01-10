#!/bin/bash


cd /data

# make sure mysql ready
./sh/wait-for-it.sh ugs-mysql:3306 -t 30 -- echo "mysql server is ready, wait for another 3 seconds to make sure the init script is done..." && sleep 3s

# run!
python ./api/main.py
