# gswitch.py - builds list of COMMANDS to run gst-switch components 

# copied from run-demo.sh
VIDEO_CAPS="video/x-raw, format=(string)I420, pixel-aspect-ratio=(fraction)1/1, width=(int)300, height=(int)200, framerate=(fraction)25/1"
AUDIO_CAPS="audio/x-raw, rate=48000, channels=2, format=S16LE, layout=interleaved"

# COMMANDS.append( Command('gst-switch-srv --record foo') )
COMMANDS.append( Command(
    'gst-switch-srv --record foo.avi -f "{}"'.format(VIDEO_CAPS)) )
    # 'gst-switch-srv --record %Y-%m-%dT%H_%M_%S.avi') )

COMMANDS.append( Command('gst-switch-ui') )

vid_src = """
gst-launch-1.0 
    videotestsrc pattern=18 is-live=1 
    ! "{}"
    ! timeoverlay font-desc="Sans 40" 
    ! clockoverlay time-format="%S" font-desc="Sans 240" 
    ! textoverlay text="s-{}" 
        halignment=2 valignment=2 font-desc="Sans 40" 
    ! gdppay 
    ! tcpclientsink port=3000 
""".replace('\n','')

COMMANDS.append( Command(vid_src.format(VIDEO_CAPS,1)) )
COMMANDS.append( Command(vid_src.format(VIDEO_CAPS,2)) )
COMMANDS.append( Command(vid_src.format(VIDEO_CAPS,3)) )

src = """
gst-launch-1.0 
    audiotestsrc
    ! "{}"
    ! queue 
    ! audioconvert
    ! gdppay 
    ! tcpclientsink port=4000 
""".replace('\n','')

COMMANDS.append( Command(src.format( AUDIO_CAPS)) )
COMMANDS.append( Command(src.format( AUDIO_CAPS)) )

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

