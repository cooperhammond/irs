import os
import argparse
from .setup_binaries import setup

parser = argparse.ArgumentParser()

parser.add_argument("-S", "--setup", dest="setup", help="Setup IRS",
                    action="store_true")

args = parser.parse_args()

if args.setup:
    setup()
    exit(0)
elif not os.path.isdir(os.path.expanduser("~/.irs")):
    print("Please run `irs --setup` to install the youtube-dl and \
ffmpeg binaries.")
else:
    from .ripper import Ripper
    Ripper  # PyLinter reasons
