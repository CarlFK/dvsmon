# vocto-prod1.py 

# dvs-mon config to run voctomix in production:
# core, gui, camera, cut, save
# remote video feeds are run out side of this set.

def main(COMMANDS,conf):
    print(conf)
    COMMANDS.append( Command('voctocore -vv'))
    COMMANDS.append( Command('voctogui -vv'))
    COMMANDS.append( Command('ingest'))
    COMMANDS.append( Command(
        'ingest --video-source blackmagichdmi --audio-source blackmagichdmi'
      ))
    COMMANDS.append( Command(
        'ingest'
        ' --video-source hdmi2usb'
        ' --audio-source pulse'
        ' --audio-dev alsa_input.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo'))
    COMMANDS.append( Command(
        'record-timestamp {dest_path}'.format(**conf)))
    COMMANDS.append( Command(
        'generate-cut-list | tee --append {dest_path}/cut-list.log'.format(
            **conf)))
    return 


def get_conf():

    import ConfigParser, os

    config = ConfigParser.RawConfigParser()
    files=config.read(os.path.expanduser('~/veyepar.cfg'))
    try:
        print(files)
        conf=dict(config.items('global'))
        dest_path = os.path.expanduser(
                '~/Videos/veyepar/{client}/{show}/dv/{room}'.format(**conf))
    except KeyError:
        dest_path = os.path.expanduser(
                '~/Videos/voctomix')
    except ConfigParser.NoSectionError:
        dest_path = os.path.expanduser(
                '~/Videos/voctomix')

    ret = {'dest_path':dest_path,
            }

    return ret

conf = get_conf()
main(COMMANDS,conf)

