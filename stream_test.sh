#!/bin/bash -x

# sencible params for testing 

# handy lines, cut/paste/un#comment:
# --show-all-detail \
#     source_fw.py \
#    source_remote_fw.py \
# /usr/bin/python2.7 ./dvs-mon.py \

python ./dvs-mon.py \
  --show-all-detail \
  --keepalive 1 \
  --commands \
    dvswitch.py \
    source_test.py \
    $*
