#!/usr/bin python

HELP = \
"""
usage:
    irs (-h | -v)
    irs [-l]
    irs -p PLAYLIST [-c COMMAND] [-l]
    irs -a ARTIST (-s SONG | -A ALBUM [-st SEARCH_TERMS]) [-c COMMAND] [-l]

Options:
  -h, --help            show this help message and exit
  -v, --version         Display the version and exit.
  -c COMMAND, --command COMMAND
                        Run a background command with each song's location.
                        Example: `-c "rhythmbox %(loc)s"`
  -a ARTIST, --artist ARTIST
                        Specify the artist name.
  -p PLAYLIST, --playlist PLAYLIST
                        Specify playlist filename. Each line in the file
                        should be formatted like so: `SONGNAME - ARTIST`
  -s SONG, --song SONG  Specify song name of the artist.
  -A ALBUM, --album ALBUM
                        Specify album name of the artist.
  -st SEARCH_TERMS, --search-terms SEARCH_TERMS
                        Only use if calling -A/--album. Acts as extra search
                        terms when looking for the album.

  -l, --choose-link     If supplied, will bring up a console choice for what
                        link you want to download based off a list of titles.
"""

import argparse
from os import system
from sys import exit
from .manage import *
from .utils import *

def console():
    system("clear")
    media = None
    while type(media) is not int:
        print (bc.HEADER)
        print ("What type of media would you like to download?")
        print ("\t1) Song\n\t2) Album")
        try:
            media = int(input(bc.YELLOW + bc.BOLD + ":: " + bc.ENDC))
        except ValueError:
            print (bc.FAIL + "\nPlease enter 1 or 2." + bc.ENDC)

    print (bc.HEADER + "Artist of song/album ", end="")
    artist = input(bc.BOLD + bc.YELLOW + ": " + bc.ENDC)

    if media == 1:
        print (bc.HEADER + "Song you would like to download ", end="")
        song = input(bc.BOLD + bc.YELLOW + ": " + bc.ENDC)
        rip_mp3(song, artist)
    elif media == 2:
        print (bc.HEADER + "Album you would like to download ", end="")
        album = input(bc.BOLD + bc.YELLOW + ": " + bc.ENDC)
        rip_album(album, artist)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true', dest='help')
    parser.add_argument('-v', '--version', dest="version", action='store_true', help="Display the version and exit.")
    parser.add_argument('-c', '--command', dest="command", help="Run a background command with each song's location.")
    parser.add_argument('-a', '--artist', dest="artist", help="Specify the artist name.")

    parser.add_argument('-l', '--choose-link', action='store_true', dest="link", \
        help="Whether or not to choose the link from a list of titles.")

    parser.add_argument('-p', '--playlist', dest="playlist", \
    help="Specify playlist filename. Each line should be formatted like so: SONGNAME - ARTIST")

    media = parser.add_mutually_exclusive_group()
    media.add_argument('-s', '--song', dest="song", help="Specify song name of the artist.")

    media.add_argument('-A', '--album', dest="album", help="Specify album name of the artist.")
    parser.add_argument('-st', '--search-terms', dest="search_terms", \
        help="Only use if calling -A/--album. Acts as extra search terms for the album.")


    args = parser.parse_args()

    if args.help:
        global HELP
        print (HELP)

    elif args.version:
        import pkg_resources
        print ("\n\n" + color("Ingenious Redistribution System", ["HEADER", "BOLD"]))
        print ("Homepage: " + color("https://github.com/kepoorhampond/irs", ["OKGREEN"]))
        print ("License: " + color("The GNU", ["YELLOW"]) + " (http://www.gnu.org/licenses/gpl.html)")
        print ("Version: " + pkg_resources.get_distribution("irs").version)

        print ("\n")
        exit(0)

    elif not args.album and args.search_terms:
        parser.error("error: must supply -A/--album if you are going to supply -st/--search-terms")
        exit(1)

    elif args.artist and not (args.album or args.song):
        print ("error: must specify -A/--album or -s/--song if specifying -a/--artist")
        exit(1)

    elif not args.artist and not args.playlist:
        console()

    elif args.playlist:
        rip_playlist(args.playlist, args.command, choose_link=args.link)

    elif args.artist:
        if args.album:
            rip_album(args.album, args.artist, command=args.command, \
                search=args.search_terms, choose_link=args.link)

        elif args.song:
            rip_mp3(args.song, args.artist, command=args.command, choose_link=args.link)



if __name__ == "__main__":
    main()
