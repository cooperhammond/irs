#!/usr/bin python
HELP = \
"""
usage:
    irs (-h | -v | -C)
    irs [-l]
    irs -p PLAYLIST [-c COMMAND] [-l]
    irs -A ALBUM [-c COMMAND] [-l]
    irs -a ARTIST -s SONG [-c COMMAND] [-l]

Options:
  -h, --help            show this help message and exit

  -v, --version         Display the version and exit.

  -C, --config          Return location of configuration file.

  -A ALBUM, --album ALBUM
                        Search spotify for an album.

  -p PLAYLIST, --playlist PLAYLIST
                        Search spotify for a playlist.

  -u USER, --user USER  Download a user playlist.

  -c COMMAND, --command COMMAND
                        Run a background command with each song's location.
                        Example: `-c "rhythmbox %(loc)s"`

  -a ARTIST, --artist ARTIST
                        Specify the artist name. Only needed for -s/--song

  -s SONG, --song SONG  Specify song name of the artist. Must be used with
                        -a/--artist

  -l, --choose-link     If supplied, will bring up a console choice for what
                        link you want to download based off a list of titles.
"""

# For exiting
from sys import exit

# Parsing args
import argparse

# Import the manager
from .manager import Manager
from .utils import *
from .config import CONFIG

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true', dest='help')
    parser.add_argument('-v', '--version', dest="version", action='store_true', help="Display the version and exit.")
    parser.add_argument('-C', '--config', dest="config", action='store_true', help="Return config file location.")

    parser.add_argument('-c', '--command', dest="command", help="Run a background command with each song's location.")
    parser.add_argument('-a', '--artist', dest="artist", help="Specify the artist name.")

    parser.add_argument('-u', '--user', dest="user", help="Specify user to download playlists from.")

    parser.add_argument('-l', '--choose-link', action='store_true', dest="link", \
        help="Whether or not to choose the link from a list of titles.")

    parser.add_argument('-p', '--playlist', dest="playlist", \
    help="Specify playlist filename. Each line should be formatted like so: SONGNAME - ARTIST")

    media = parser.add_mutually_exclusive_group()
    media.add_argument('-s', '--song', dest="song", help="Specify song name of the artist.")

    media.add_argument('-A', '--album', dest="album", help="Specify album name of the artist.")


    args = parser.parse_args(sys.argv[1:] + CONFIG["default_flags"].split(" ")[:-1])

    manager = Manager(args)

    if args.help:
        global HELP
        print (HELP)
        exit(1)

    elif args.version:
        import pkg_resources
        print ("\n\n" + color("Ironic Redistribution System", ["HEADER", "BOLD"]))
        print ("Homepage: " + color("https://github.com/kepoorhampond/irs", ["OKGREEN"]))
        print ("License: " + color("GNU", ["YELLOW"]) + " (http://www.gnu.org/licenses/gpl.html)")
        print ("Version: " + pkg_resources.get_distribution("irs").version)
        print ("\n")
        exit(0)

    elif args.config:
        print (get_config_file_path())

    #elif args.artist and not (args.album or args.song):
    #    parser.error("error: must supply -A/--album or -s/--song if specifying -a/--artist")
    #    exit(1)

    elif args.playlist:
        manager.rip_spotify_list("playlist")

    elif args.user:
        manager.rip_spotify_list("user")

    elif args.album:
        manager.rip_spotify_list("album")

    elif args.song:
        manager.rip_mp3()

    else:
        manager.console()

if __name__ == "__main__":
    main()
