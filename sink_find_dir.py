#!/usr/bin/python

# find a place to save files
# look for ~/Videos, then /media/disk, then /media/*

# also check for ~/veyepar.cfg
#  if found: use client/show slugs to construct dir name
#  else: use $hostname

import os
import socket
import ConfigParser

# make a list of dirs to search -
# use any that have a dv or veyepar dir
# else find the 'best' one.
# home dir
dirs  = [os.path.expanduser('~/Videos')]
# if can't find a Video dir, start looking for anything reasonable.
# someday maybe search for something with the most free space.
# ubuntu now mounts drives under /media/$USER/disk-lable
# need to support the $USER thing someday?

def find_Vdirs(root, dirs):
    """ find dir/Videos dirs in root (does not walk the tree) """
    import os
    if os.path.exists(root):
        for d in os.listdir(root):
            d2 = os.path.join(root,d,'Videos')
            if os.path.exists(d2):
                dirs.append(d2)
     
# dirs += ["/media/%s/Videos"%dir 
#         for dir in os.listdir('/media') 
#          if dir[0]!='.' ]

# check for /media/(disk name)/Videos
find_Vdirs('/media', dirs)
       
# check /media/(user)/(disk name)/Videos
find_Vdirs(os.path.join('/media',os.getlogin()),dirs)

# checi ~/mnt/(server)/Videos
find_Vdirs(os.path.join(os.path.expanduser('~'),"mnt"),dirs)

# rom excludes cdrom cdrom-1 or any other rom.
for dir in os.listdir('/media'):
    if (dir[0]!='.'
        and 'rom' not in dir
        and 'floppy' not in dir):
            # if we get here, I hope it isn't the live CD.
            # dirs.append("/media/%s"%dir)
            pass

# dirs.append(os.path.expanduser('~'))

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
                # break
            else:
                print "%s minutes is not enough." % (minutes)

# vid_dir is the trunk
# if veyepar is around, use it
# if veyepar room isn't set, use hostname
hostname=socket.gethostname() 

config = ConfigParser.RawConfigParser()
files=config.read([os.path.expanduser('~/veyepar/dj/scripts/veyepar.cfg'),
        os.path.expanduser('~/veyepar.cfg')])
if files:
    d=dict(config.items('global'))
    client = d['client']
    show = d['show']
    loc = d.get('room',hostname)
    dv_dir = os.path.join( 'veyepar', client, show, 'dv', loc )
else:
    dv_dir = os.path.join( 'dv', hostname )

# add output dirs
for vid_dir in vid_dirs:
    print "vid_dir", vid_dir
    COMMANDS.append(
        Command('dvsink-files %s %s' % (
                os.path.join( vid_dir, dv_dir, '%Y-%m-%d','%H_%M_%S.dv' ),
                hostport,
                )))

# os.path.join( vid_dir, 'dv', hostname,'%Y-%m-%d','%H_%M_%S.dv' ),

