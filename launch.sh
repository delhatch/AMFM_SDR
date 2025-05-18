#!/bin/bash

cd /home/drh

sleep 1

#echo "Starting launch.sh at $(date)" >> launch.log
#echo "DISPLAY=$DISPLAY" >> launch.log

#ip link show lo >> launch.log 2>&1

#echo "Starting the SDR Radio app."
#python3 AMFM_radio_v1.py >> launch.log 2>&1 &
python3 AMFM_radio_v1.py &
#echo "Ended at $(date)" >> launch.log

sleep 10

#echo "Port 8080 status: " >> launch.log
#netstat -tuln | grep 8080 >> launch.log 2>&1

#echo "Starting control app at $(date)" >> launch.log
#echo "Starting the control app."
#python3 radio_control_v21.py >> launch.log 2>&1 &
python3 radio_control_v21.py &

#echo "Ended at $(date)" >> launch.log
