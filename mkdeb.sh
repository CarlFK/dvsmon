#!/bin/bash -x
rm ../*.changes
export DEBFULLNAME="Carl Karsten"
export DEBEMAIL=carl@personnelware.com
debchange --increment $0
debuild -S -sa 
cd ..
dput CarlFK-ppa *.changes

