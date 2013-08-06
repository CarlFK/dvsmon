#!/bin/bash -x

pkill dvswitch
sleep 1
# dvs=$! saves the pid 
DISPLAY=:0 dvswitch --host 0.0.0.0 --port 8003 & dvs=$!
echo to kill dvswitch:
echo kill $dvs 
sleep 3
dvsource-file --host 0.0.0.0 --port 8003 -l app_data/dv/test-1.dv
sleep 1
kill $dvs

