import os
import argparse
from .setup_binaries import setup

parser = argparse.ArgumentParser()

parser.add_argument("-S", "--setup", dest="setup", help="Setup IRS",
                    action="store_true")

args, unknown = parser.parse_known_args()

if args.setup:
    setup()
    exit(0)
elif not os.path.isdir(os.path.expanduser("~/.irs")):
    print("Please run `irs --setup` to install the youtube-dl and \
ffmpeg binaries.")
    exit(1)
else:
    from .ripper import Ripper
    Ripper
