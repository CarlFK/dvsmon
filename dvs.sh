#!/bin/bash -ix

cd $(dirname $0)

# sencible params for production (recording talks) 

./dvs-mon.py -c \
    dvswitch-schroot.py \
    source_alsa.py \
    source_remote_fw.py \
    source_remote_usb.py \
    sink_find_dir.py 

#  dvswitch.py \
#    source_fw.py \
# --host 130.216.0.$1 --port 1234
