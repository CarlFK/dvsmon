#!/bin/bash -x

# First shot at gst-switch control
PATH="`pwd`/../gst-switch/tools:$PATH"

./dvs-mon.py -c gswitch.py 

