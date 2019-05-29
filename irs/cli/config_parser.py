import os
import sys

import yaml


def parse_config():
    """Parses config using environment variables."""

    home = os.environ.get("HOME") or os.path.expanduser("~/")

    check_for_and_set("irs_config_dir", home + "/.irs", None)

    check_for = [home + "/.irs/config.yml", home + "/.irs/bin/ffmpeg", 
        home + "/.irs/bin/ffprobe"]

    for path in check_for:
        if not os.path.exists(path):
            print("There's no config set up. Set up a configuration folder by "
                "running `irs --setup`")
            sys.exit(1)

    config = {}

    with open(os.environ["irs_config_dir"] + "/config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    check_for_and_set("SPOTIFY_CLIENT_ID", config.get(
        "SPOTIFY_KEYS").get("CLIENT_ID"), None)
    check_for_and_set("SPOTIFY_CLIENT_SECRET", config.get(
        "SPOTIFY_KEYS").get("CLIENT_SECRET"), None)

    check_for_and_set("irs_music_dir", os.path.expanduser(config.get("music_directory")), 
        home + "/Music")
    check_for_and_set("irs_ffmpeg_dir", os.environ["irs_config_dir"] + "/bin", None)


def check_for_and_set(key, val, else_):
    """Checks for an environment variable and if it doesn't exist, then set it
    equal to the val given.
    :param key: string, key to check for existence
    :param val: value to replace key value with if it doesn't exists
    :param else_: if val doesn't exist, use else_ instead
    """
    if not os.environ.get(key):
        if key:
            os.environ[key] = val
        else:
            os.environ[key] = else_
