# MP3 Metadata editing
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

# Info finding
from urllib.parse import quote_plus, quote
from urllib.request import urlopen, Request

# Info parsing
import json
from re import match
from bs4 import BeautifulSoup

# Local utils
from .utils import *

# Powered by...
import spotipy

class Metadata:
    def __init__(self, location, song, artist):
        self.spotify = spotipy.Spotify()

        self.song = song
        self.artist = artist
        self.location = location

        self.info = self.search_google()
        self.mp3 = MP3(self.location, ID3=EasyID3)

    def get_attr(self, attr):
        try:
            return self.mp3[attr][0]
        except Exception:
            return False

    def add_title(self):
        self.mp3['title'] = self.song
        self.mp3.save()
        return True


    def add_artist(self):
        self.mp3['artist'] = self.artist
        self.mp3.save()
        return True


    def add_album(self, album=None):
        try:
            if not album:
                for i, j in enumerate(self.info):
                    if "Album:" in j:
                        album = (self.info[i + 1])

            self.mp3['album'] = album
            self.mp3.save()
            return True

        except Exception:
            self.mp3['album'] = self.song
            self.mp3.save()
            return False


    def add_release_date(self, release_date=None):
        try:
            if not release_date:
                for i, j in enumerate(self.info):
                    if "Released:" in j:
                        date = (self.info[i + 1])

            self.mp3['date'] = date
            self.mp3.save()
            return True
        except UnboundLocalError:
            return False


    def add_track_number(self, track_number):
        self.mp3['tracknumber'] = str(track_number)
        self.mp3.save()
        return True


    def add_album_art(self, image_url):
        mp3 = EasyMP3(self.location, ID3=ID3)

        try:
            mp3.add_tags()
        except Exception as e:
            pass

        if not image_url:
            image_url = self.get_albumart_url(album)

        mp3.tags.add(
            APIC(
                encoding = 3,
                mime = 'image/png',
                type = 3,
                desc = 'cover',
                data = urlopen(image_url).read()
            )
        )
        mp3.save()
        return image_url


    def search_google(self, search_terms=""):
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif match('<!--.*-->', str(element)):
                return False
            return True

        search_terms = "%s %s %s" % (self.song, self.artist, search_terms)
        url = 'http://www.google.com/search?q=' + quote_plus(search_terms)

        hdr = {
            'User-Agent':'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        texts = BeautifulSoup(urlopen(Request(url, \
            headers=hdr)).read(), 'html.parser').findAll(text=True)

        return list(filter(visible, texts))
