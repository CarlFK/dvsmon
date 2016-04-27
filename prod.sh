#!/bin/bash -ix

# sencible params for production (recording talks) 

cd $(dirname $0)
dvs_dir=$PWD

vocto_dir="${1:-~/voctomix}"
cd $vocto_dir

$dvs_dir/dvs-mon.py -c \
    $dvs_dir/vocto-prod1.py

