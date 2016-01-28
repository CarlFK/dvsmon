#!/usr/bin/python

import os

"""
# maybe figure out what card to use?
# personaly I like the idea of it failing if it can't find the
# one we expect.  falling back to on board sound will be confusing.

cat /proc/asound/cards

carl@dc10:~/src/dvs/dvswitch/src$ cat /proc/asound/cards
 0 [Intel          ]: HDA-Intel - HDA Intel
                      HDA Intel at 0xd4720000 irq 47
 1 [Device         ]: USB-Audio - USB PnP Audio Device
                      C-Media Electronics Inc. USB PnP Audio Device at usb-0000:00:1d.0-1.2, full spe
"""


# get list of sound cards
with open('/proc/asound/cards') as proc_sound_cards:
    cards = proc_sound_cards.read()

# find the last one
#   .strip to remvoe the trailing \n
cards = cards.strip().split('\n')
last_card = cards[-2]
hw = last_card.split()[0]

# super hack - ThinkPad has some sound device we need to ignore
if hw=='29':
    last_card = cards[-4]
    hw = last_card.split()[0]

hw = os.environ['VOC_ALSA_DEV']

COMMANDS.append( Command('dvsource-alsa -s pal -a 16:9 -r 48000 hw:%s %s' % (hw,hostport,)))
# COMMANDS.append( 'dvsource-alsa -s ntsc -r 48000 hw:0 %s' % (hostport,))


