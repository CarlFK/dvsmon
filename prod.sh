#!/bin/bash -ix

cd $(dirname $0)
dvsdir=$PWD

cd ~/voctomix

# sencible params for production (recording talks) 

$dvsdir/dvs-mon.py -c \
    $dvsdir/vocto-all.py

echo \
    vocto-core.py \
    vocto-gui.py \
    vocto-src-cam.py \
    vocto-src-grab.py \
    vocto-sink-file.py

#  dvswitch.py \
#    source_fw.py \
# --host 130.216.0.$1 --port 1234
