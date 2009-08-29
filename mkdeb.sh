#!/bin/bash -x
rm ../*.changes
export DEBFULLNAME="Carl Karsten"
export DEBEMAIL=carl@personnelware.com
debchange --increment $1
debuild -S -sa 
cd ..
dput CarlFK-ppa *.changes

