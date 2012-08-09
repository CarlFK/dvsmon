#!/bin/bash -x

# bug_1.sh
# demos the blocking bug.  at least I think it is blocking.

/usr/bin/python ./dvs-mon.py \
  --host localhost --port 2000 \
  --commands \
    dvswitch.py \
    test_spew.py \
  --keepalive 100 \
  --show-all-detail \
    $*
