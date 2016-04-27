#!/bin/bash -x

# sencible params for testing 

cd $(dirname $0)
dvsdir=$PWD

cd ~/voctomix

# handy lines, cut/paste/un#comment:
# --show-all-detail \

python ./dvs-mon.py \
  -c vocto-test.py

exit
# Bye bye DVswitch, it was a good 10 years.
# we will miss you.
python ./dvs-mon.py \
  -c \
    dvswitch.py \
    dvswitch-schroot.py \
    source_test.py \
    source_alsa.py \
    sink_find_dir.py \
    sink_ffplay.py \
    source_remote_usb.py \
    source_remote_fw.py \
    $*
