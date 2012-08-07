#!/bin/bash -x

# bug_1.sh
# demos the blocking bug.  at least I think it is blocking.

/usr/bin/python2.7 ./dvs-mon.py \
  --host localhost --port 2000 \
  --commands \
    dvswitch.py \
    source_alsa.py \
  --keepalive 100 \
  --show-all-detail \
    $*
