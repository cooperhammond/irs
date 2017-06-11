import sys
from os import path

if path.isfile(path.expanduser("~/.irs/config_.py")):
    sys.path.append(path.expanduser("~/.irs"))  # Add config to path

    import config_  # from "~/.irs/config_.py"

    CONFIG = config_.CONFIG
else:
    config = open("irs/config_preset", "r").read()
    print(config)
    CONFIG = eval(config)
