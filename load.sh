#!/bin/bash -x
for ((i=1; i<=30; i++)); do 
  screen -d -m dvsource-file -l test-2.dv 
done
