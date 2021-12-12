#!/bin/bash
clear > /dev/tty1
cd /home/pi/callid/backend/datagos_svc/ || exit
source /home/pi/callid/backend/venv/bin/activate
python3 /home/pi/callid/backend/datagos_svc/datagos_server.py
