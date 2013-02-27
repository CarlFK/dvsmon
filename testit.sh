#!/bin/bash -x

# sencible params for testing 

# handy lines, cut/paste/un#comment:
# --show-all-detail \
#     source_fw.py \
#    source_remote_fw.py \
# /usr/bin/python2.7 ./dvs-mon.py \

python ./dvs-mon.py \
  -c \
    dvswitch.py \
    source_alsa.py \
    source_test.py \
    sink_ffplay.py \
    sink_find_dir.py \
    $*
