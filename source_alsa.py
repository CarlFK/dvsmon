#!/usr/bin/python

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

# hw='0'

# get list of sound cards
with open('/proc/asound/cards') as proc_sound_cards:
    cards = proc_sound_cards.read()

# find the last one
#   .strip to remvoe the trailing \n
cards = cards.strip().split('\n')
print cards
last_card = cards[-2]
print last_card
hw = last_card.split()[0]
print hw

COMMANDS.append( Command('dvsource-alsa -s ntsc -r 48000 hw:%s %s' % (hw,hostport,)))
# COMMANDS.append( 'dvsource-alsa -s ntsc -r 48000 hw:0 %s' % (hostport,))


