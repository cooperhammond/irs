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

def search_google(song, artist, search_terms=""):

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif match('<!--.*-->', str(element)):
            return False
        return True

    string = "%s %s %s" % (song, artist, search_terms)
    filename = 'http://www.google.com/search?q=' + quote_plus(string)
    hdr = {
        'User-Agent':'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    texts = BeautifulSoup(urlopen(Request(filename, \
        headers=hdr)).read(), 'html.parser').findAll(text=True)

    return list(filter(visible, texts))

def parse_metadata(song, artist, location, filename, tracknum="", album="", album_url=None):
    googled = search_google(song, artist)

    mp3file = MP3("%s/%s" % (location, filename), ID3=EasyID3)

    # Song title
    mp3file['title'] = song
    mp3file.save()

    print("")
    print (bc.OKGREEN + "Title parsed: " + bc.ENDC + mp3file['title'][0])

    # Artist
    mp3file['artist'] = artist
    mp3file.save()

    print (bc.OKGREEN + "Artist parsed: " + bc.ENDC + mp3file['artist'][0])

    # Album
    if album == "":
        for i, j in enumerate(googled):
            if "Album:" in j:
                album = (googled[i + 1])
    if album:
        mp3file['album'] = album
        print (bc.OKGREEN + "Album parsed: " + bc.ENDC + mp3file['album'][0])
    else:
        print (bc.FAIL + "Album not parsed.")

    mp3file.save()

    # Release date
    for i, j in enumerate(googled):
        if "Released:" in j:
            date = (googled[i + 1])

    try:
        mp3file['date'] = date
        print (bc.OKGREEN + "Release date parsed: " + bc.ENDC + mp3file['date'][0])
    except Exception:
        mp3file['date'] = ""
        pass

    mp3file.save()

    # Track number
    if tracknum != "":
        mp3file['tracknumber'] = str(tracknum)
        mp3file.save()

    # Album art
    try:
        if album_url == None:
            album_url = get_albumart_url(album, artist)
            embed_mp3(album_url, location + "/" + filename)
        else:
            embed_mp3(album_url, location + "/" + filename)

        print (bc.OKGREEN + "Album art parsed: " + bc.ENDC + album_url)

    except Exception as e:
        print (e)
        print (bc.FAIL + "Album art not parsed." + bc.ENDC)

def embed_mp3(albumart_url, song_location):
    image = urlopen(albumart_url)
    audio = EasyMP3(song_location, ID3=ID3)

    try:
        audio.add_tags()
    except Exception as e:
        pass

    audio.tags.add(
        APIC(
            encoding = 3,
            mime = 'image/png',
            type = 3,
            desc = 'Cover',
            data = image.read()
        )
    )
    audio.save()

def get_albumart_url(album, artist):
    album = "%s %s Album Art" % (artist, album)
    url = ("https://www.google.com/search?q=" + quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
    header = {
        'User-Agent':
            '''
                Mozilla/5.0 (Windows NT 6.1; WOW64)
                AppleWebKit/537.36 (KHTML,like Gecko)
                Chrome/43.0.2357.134 Safari/537.36
            '''
    }

    soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

    albumart_div = soup.find("div", {"class": "rg_meta"})
    albumart = json.loads(albumart_div.text)["ou"]

    return albumart
