import sys
from os import path


sys.path.append(path.expanduser("~/.irs"))  # Add config to path

import config_  # from "~/.irs/config_.py"

CONFIG = config_.CONFIG
