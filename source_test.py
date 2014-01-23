#!/usr/bin/python

import os


# https://github.com/timvideos/dvsource-v4l2-other
cmd = "dvsource-v4l2-other -s ntsc --fake ball"
description = "gstreamer ball and buzz"
COMMANDS.append( Command( cmd, description ))
cmd = "dvsource-v4l2-other -s ntsc --fake snow"
description = "gstreamer snow and buzz"
COMMANDS.append( Command( cmd, description ))
            
# find dir of test files
    # check in propper installed dir, or in the local dir for dev
dirs=['/usr/share/dvsmon/dv/','app_data/dv/']
for d in dirs:
    if os.path.exists( d ):
        for i in '12':
            test_dv = 'test-%s.dv' % (i)
            fullpath=os.path.join(d,test_dv )

            cmd = 'dvsource-file -l %s %s'%(fullpath,hostport)
            description = test_dv
            COMMANDS.append( Command( cmd, description ))

        # once files have been found in one of the dirs, stop looking.
        exit

