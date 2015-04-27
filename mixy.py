# gswitch.py - builds list of COMMANDS to run gst-switch components 

# COMMANDS.append( Command('gst-switch-srv --record foo') )
COMMANDS.append( Command(
    'gst-switch-srv --record foo.avi') )
    # 'gst-switch-srv --record %Y-%m-%dT%H_%M_%S.avi') )

COMMANDS.append( Command('gst-switch-ui') )

vid_src = """
gst-launch-1.0 
    videotestsrc pattern=18 is-live=1 
    ! video/x-raw, width=300, height=200 
    ! timeoverlay font-desc="Sans 40" 
    ! clockoverlay time-format="%S" font-desc="Sans 240" 
    ! textoverlay text="s-{}" 
        halignment=2 valignment=2 font-desc="Sans 40" 
    ! gdppay 
    ! tcpclientsink port=3000 
""".replace('\n','')

COMMANDS.append( Command(vid_src.format(1)) )
COMMANDS.append( Command(vid_src.format(2)) )
COMMANDS.append( Command(vid_src.format(3)) )

src = """
gst-launch-1.0 
    audiotestsrc
    ! queue 
    ! audioconvert
    ! gdppay 
    ! tcpclientsink port=4000 
""".replace('\n','')

COMMANDS.append( Command(src) )
COMMANDS.append( Command(src) )

vid_src = """
gst-launch-1.0 v4l2src device=/dev/video0 \
        ! decodebin \
        ! videorate \
        ! videoconvert \
        ! videoscale add-borders=1 \
        ! video/x-raw,format=I420,width=300,height=200,framerate=25/1 \
        ! gdppay \
        ! tcpclientsink port=3000
""".replace('\n','')

COMMANDS.append( Command(vid_src) )

