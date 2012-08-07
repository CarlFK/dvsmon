#!/bin/bash -x

# sencible params for testing 

# --show-all-detail \
#     source_fw.py \
/usr/bin/python2.7 ./dvs-mon.py \
  -c \
    dvswitch.py \
    source_alsa.py \
    source_test.py \
    source_remote_fw.py \
    sink_ffplay.py \
    sink_find_dir.py \
    $*
