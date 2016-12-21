# MP3 Metadata editing
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

# Info getting
from urllib.parse import quote_plus, quote
from urllib.request import urlopen, Request

# Info parsing
import json
from re import match
from bs4 import BeautifulSoup

# Local utils
from .utils import *

class Metadata:
    def __init__(self, song, artist, location):
        self.song = song
        self.artist = artist
        self.location = location

        self.info = search_google(song, artist)
        self.mp3 = MP3("%s/%s" % (location, filename), ID3=EasyID3)


    def parse_title():
        self.mp3['title'] = self.song
        self.mp3.save()
        print (bc.OKGREEN + "Title parsed: " + bc.ENDC + self.mp3['title'][0])

    def parse_artist():
        self.mp3['artist'] = self.artist
        self.mp3.save()
        print (bc.OKGREEN + "Artist parsed: " + bc.ENDC + self.mp3['artist'][0])

    def parse_album(album=None):
        try:
            if not album:
                for i, j in enumerate(self.info):
                    if "Album:" in j:
                        album = (self.info[i + 1])
        except Exception as e:
            album = None

        if album:
            self.mp3['album'] = album
            print (bc.OKGREEN + "Album parsed: " + bc.ENDC + self.mp3['album'][0])
        else:
            print (bc.FAIL + "Album not parsed.")

        self.mp3.save()

    def parse_release_date():
        for i, j in enumerate(self.info):
            if "Released:" in j:
                date = (self.info[i + 1])

        try:
            self.mp3['date'] = date
            print (bc.OKGREEN + "Release date parsed: " + bc.ENDC + self.mp3['date'][0])
        except Exception:
            self.mp3['date'] = ""
            pass

        self.mp3.save()

    def search_google(self, song, artist, search_terms=""):

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif match('<!--.*-->', str(element)):
                return False
            return True

        search_terms = "%s %s %s" % (song, artist, search_terms)
        url = 'http://www.google.com/search?q=' + quote_plus(string)

        hdr = {
            'User-Agent':'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        texts = BeautifulSoup(urlopen(Request(filename, \
            headers=hdr)).read(), 'html.parser').findAll(text=True)

        return list(filter(visible, texts))
