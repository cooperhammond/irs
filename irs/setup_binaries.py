import ydl_binaries
from shutil import copyfile
import os
import inspect
import irs


def setup():
    ydl_binaries.download_ffmpeg("~/.irs/bin/")
    ydl_binaries.update_ydl("~/.irs/bin/")

    config_file = os.path.expanduser("~/.irs/config_.py")
    if not os.path.isfile(config_file):
        print("\n")
        os.system("ls " + os.path.dirname(inspect.getfile(irs)))
        print(inspect.getfile(irs))
        print("\n")
        copyfile(os.path.dirname(inspect.getfile(irs)) + "/config_preset.py",
                 config_file)
