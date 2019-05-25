import sys
import os

import argparse

from .song import Song
from .album import Album
from .playlist import Playlist

def main():
    """
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--artist", dest="artist", 
        help="Specify artist name. Must be used with -s/--song or -A/--album")

    parser.add_argument("-s", "--song", dest="song", 
        help="Specify song name. Must be used with -a/--artist")

    parser.add_argument("-A", "--album", dest="album",
        help="Specify album name. Can be used by itself.")

    parser.add_argument("-p", "--playlist", dest="playlist",
        help="Specify playlist name. Must be used with -A/--album")

    parser.add_argument("-u", "--username", dest="username",
        help="Specify user name for playlist. Must be used with -A/--album")

    parser.add_argument("-o", "--organization", dest="organization", 
        default="standard", help="Specify type of organization for list."
        "Used when downloading spotify playlist/album")

    args = parser.parse_args()

    set_local_env()

    if args.song and args.artist: # single song
        Song(args.song, args.artist).grab_it()
    elif args.album and args.artist: # album with an artist
        Album(args.album, args.artist).grab_it()
    elif args.album: # album without artist
        Album(args.album).grab_it()
    elif args.playlist and args.username: # playlist
        Playlist(args.playlist, args.username, args.organization).grab_it()


def set_local_env():
    os.environ["irs_music_dir"] = os.path.join(
        os.environ["HOME"], "Audio"
    )