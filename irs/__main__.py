#!/usr/bin python
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--artist', dest="artist", help="Specify the artist name")
    parser.add_argument('-v', '--version', dest="version", action='store_true', help="Display the version and exit.")

    media = parser.add_mutually_exclusive_group()
    media.add_argument('-A', '--album', dest="album", help="Specify album name of the artist")
    media.add_argument('-s', '--song', dest="song", help="Specify song name of the artist")

    args = parser.parse_args()


    if args.version:
        import pkg_resources
        print ("\n\n" + color("Ingenious Redistribution System", ["HEADER", "BOLD"]))
        print ("Homepage: " + color("https://github.com/kepoorhampond/irs", ["OKGREEN"]))
        print ("License: " + color("The GNU", ["YELLOW"]) + " (http://www.gnu.org/licenses/gpl.html)")
        print ("Version: " + pkg_resources.get_distribution("irs").version)

        print ("\n")
        exit(0)

    if args.artist and not (args.album or args.song):
        print ("usage: __init__.py [-h] [-a ARTIST] [-A ALBUM | -s SONG] \n\
    error: must specify -A/--album or -s/--song if specifying -a/--artist")
        exit(1)

    elif not args.artist:
        console()

    elif args.artist:
        if args.album:
            rip_album(args.album, args.artist)
        elif args.song:
            rip_mp3(args.song, args.artist)

if __name__ == "__main__":
    main()
