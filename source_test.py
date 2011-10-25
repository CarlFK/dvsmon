#!/usr/bin/python

import os

# find test files
for i in '12': 
    test_dv = 'test-%s.dv' % (i)
    # check in propper installed dir, or in the local dir for dev
    dirs=['/usr/share/dvsmon/dv/','app_data/dv/']
    for d in dirs:
        fullpath=os.path.join(d,test_dv )
        if os.path.exists( fullpath ):
            COMMANDS += [ 'dvsource-file %s -l %s'%(hostport,fullpath) ]
            exit

