# MP3 Metadata editing
from mutagen.mp3 import EasyMP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import *  # There's A LOT of stuff to import, forgive me.
from mutagen.id3 import APIC, ID3

# System
import sys

# Powered by...
import spotipy

# Local utils
from .utils import ObjManip
om = ObjManip

# Info finding
if sys.version_info[0] >= 3:
    from urllib.parse import quote_plus, quote
    from urllib.request import urlopen, Request
elif sys.version_info[0] < 3:
    from urllib import quote_plus, quote
    from urllib import urlopen
    from urllib2 import Request


class Metadata:
    def __init__(self, location):
        self.spotify = spotipy.Spotify()
        self.location = location
        self.mp3 = EasyID3(self.location)
        EasyID3.RegisterTextKey("comment", "COMM")

    def add_tag(self, tag, data):
        # For valid tags: `EasyID3.valid_keys.keys()`
        self.mp3[tag] = data
        self.mp3.save()

    def read_tag(self, tag):
        try:
            return self.mp3[tag]
        except Exception:
            return []

    def add_album_art(self, image_url):
        mp3 = EasyMP3(self.location, ID3=ID3)
        mp3.tags.add(
            APIC(
                encoding = 3,
                mime     = 'image/png',
                type     = 3,
                desc     = 'cover',
                data     = urlopen(image_url).read()
            )
        )
        mp3.save()


def find_album_and_track(song, artist, spotify=spotipy.Spotify()):
    tracks = spotify.search(q=song, type="track")["tracks"]["items"]

    for track in tracks:
        if om.blank_include(track["name"], song):
            if om.blank_include(track["artists"][0]["name"], artist):
                return track["album"], track
    return False, False


def parse_genre(genres):
    if genres != []:
        genres.reverse()
        genres = list(map(lambda x: x.replace("-", " "), genres))
        genres.sort(key=lambda x: len(x.split()))
        return genres[0].title()
    else:
        return ""
