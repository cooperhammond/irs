import ydl_binaries
from shutil import copyfile
import os
import inspect
import irs


def setup():
    bin_path = os.path.expanduser("~/.irs/bin/")

    ydl_binaries.download_ffmpeg(bin_path)
    ydl_binaries.update_ydl(bin_path)

    config_file = os.path.expanduser("~/.irs/config_.py")
    if not os.path.isfile(config_file):
        copyfile(os.path.dirname(inspect.getfile(irs)) + "/config_preset.py",
                 config_file)
