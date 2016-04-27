#!/bin/bash -ix

# sencible params for production (recording talks) 

# $1 is the dir voctomix is in.  defaults to the dir dvsmon is in.

cd $(dirname $0)
dvs_dir=$PWD

cd ..
vocto_dir="${1:-voctomix}"
cd $vocto_dir

$dvs_dir/dvs-mon.py -c \
    $dvs_dir/vocto-prod1.py

