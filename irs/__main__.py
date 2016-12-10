#!/usr/bin python
import argparse
from .manage import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--artist', dest="artist", help="Specify the artist name")

    media = parser.add_mutually_exclusive_group()
    media.add_argument('-A', '--album', dest="album", help="Specify album name of the artist")
    media.add_argument('-s', '--song', dest="song", help="Specify song name of the artist")

    args = parser.parse_args()

    if args.artist and not (args.album or args.song):
        print ("usage: __init__.py [-h] [-a ARTIST] [-A ALBUM | -s SONG] \n\
    error: must specify -A/--album or -s/--song if specifying -a/--artist")
        sys.exit(1)

    elif not args.artist:
        console

    elif args.artist:
        if args.album:
            rip_album(args.album, args.artist)
        elif args.song:
            rip_mp3(args.song, args.artist)

if __name__ == "__main__":
    main()
