#!/usr/bin/python

COMMANDS.append( Command('voctocore -vv'))
COMMANDS.append( Command('voctogui -vv'))
COMMANDS.append( Command('ingest'))
COMMANDS.append( Command(
    'ingest'
    ' --video-source hdmi2usb'
    ' --audio-source pulse'
    ' --audio-dev alsa_input.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo'))
COMMANDS.append( Command('record-timestamp.sh'))
COMMANDS.append( Command('example-scripts/control-server/generate-cut-list.py | tee --append /home/juser/Videos/veyepar/ps1/2016Apr300sof/dv/cnt3/cut-list.log'))



