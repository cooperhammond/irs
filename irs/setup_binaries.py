import ydl_binaries
from shutil import copyfile
import os


def setup():
    ydl_binaries.download_ffmpeg("~/.irs/bin/")
    ydl_binaries.update_ydl("~/.irs/bin/")

    config_file = os.path.expanduser("~/.irs/config_.py")
    if not os.path.isfile(config_file):
        copyfile("irs/config_preset", config_file)
