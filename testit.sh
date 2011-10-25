#!/bin/bash -x

# sencible params for testing 

./dvs-mon.py -c dvswitch.py source_alsa.py source_fw.py source_test.py sink_find_dir.py sink_ffplay.py $*
