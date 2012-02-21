#!/usr/bin/python

# find a place to save files
# look for ~/Videos, then /media/disk, then /media/*

import os
import socket

# make a list of dirs to search -
# use any that have a dv or veyepar dir
# else find the 'best' one.
# home dir
dirs  = [os.path.expanduser('~/Videos/veyepar')]
# anyting mounted under /media with a Videos/veyepar dir
dirs += ["/media/%s/Videos/veyepar"%dir for dir in os.listdir('/media') if dir[0]!='.' ]
# can't find a veyepar dir. now start looking for anything reasonable.
# someday maybe search for something with the most free space.
dirs += ["/media/%s/Videos"%dir for dir in os.listdir('/media') if dir[0]!='.' ]
dirs += [os.path.expanduser('~/Videos')]
# rom excludes cdrom cdrom-1 or any other rom.
dirs += ["/media/%s"%dir
    for dir in os.listdir('/media') \
        if (dir[0]!='.'
            and 'rom' not in dir
            and 'floppy' not in dir) ]
# if we get here, I hope it isn't the live CD.
dirs += [os.path.expanduser('~')]

print "dirs to check:", dirs

vid_dirs=[]
for vid_dir in dirs:
    print "checking", vid_dir
    if os.path.exists(vid_dir):
        print "found, checking for write perms..."
        w_perm = os.access(vid_dir, os.W_OK)
        print 'os.access("%s", os.W_OK): %s'%( vid_dir, w_perm )
        if w_perm:
            s=os.statvfs(vid_dir)
            print 'block size: %s' % s.f_bsize
            print 'free blocks: %s' % s.f_bavail
            gigfree=s.f_bsize * s.f_bavail / 1024.0**3
            minutes = gigfree/.23
            print 'free space: %s gig' % round(gigfree,1)
            print 'room for: %s min' % round(minutes,1)
            if minutes>5:
                vid_dirs.append(vid_dir)
                break
            else:
                print "%s minutes is not enough." % (minutes)

hostname=socket.gethostname()

# add output dirs
for vid_dir in vid_dirs:
    COMMANDS.append(
        Command('dvsink-files %s %s' % (
                os.path.join( vid_dir, 'dv', hostname,'%Y-%m-%d','%H_%M_%S.dv' ),
                hostport,
                )))

