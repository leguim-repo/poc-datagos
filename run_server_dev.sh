#!/bin/bash

parent=$(pwd)
PYTHONPATH=$PYTHONPATH:$parent:"$parent/server"
export PYTHONPATH
echo $PYTHONPATH

DB_HOST="127.0.0.1"
DB_PORT="8306"
export DB_HOST
export DB_PORT
python server/datagos_server.py
