#!/usr/bin/python

COMMANDS.append( Command('voctocore/voctocore.py -vv'))
COMMANDS.append( Command('voctogui/voctogui.py -vv'))
COMMANDS.append( Command('example-scripts/gstreamer/ingest.py'))
COMMANDS.append( Command(
    # 'clients/source/ingest.py'
    'example-scripts/gstreamer/ingest.py'
    ' --video-source hdmi2usb'
    ' --audio-source pulse'
    ' --audio-dev alsa_input.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo'))
COMMANDS.append( Command('record-timestamp.sh'))
COMMANDS.append( Command('example-scripts/control-server/generate-cut-list.py | tee --append /home/juser/Videos/veyepar/ps1/2016Apr300sof/dv/cnt3/cut-list.log'))



