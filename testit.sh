#!/bin/bash -x

# sencible params for testing 

# --show-all-detail \
#     source_fw.py \
./dvs-mon.py \
  -c \
    dvswitch.py \
    source_test.py \
    source_remote_fw.py \
    source_alsa.py \
    sink_ffplay.py \
    sink_find_dir.py \
    $*
