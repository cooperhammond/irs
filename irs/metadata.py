import mutagen.id3, mutagen.easyid3, mutagen.mp3
import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import requests
from .utils import *
import re

def search_google(song, artist, search_terms=""):
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True
    string = "%s %s %s" % (song, artist, search_terms)
    filename = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(string)
    hdr = {
    'User-Agent':'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    texts = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(filename, \
    headers=hdr)).read(), 'html.parser').findAll(text=True)
    return list(filter(visible, texts))

def parse_metadata(song, artist, location, filename, tracknum="", album=""):
    googled = search_google(song, artist)
    mp3file = mutagen.mp3.MP3("%s/%s" % (location, filename), ID3=mutagen.easyid3.EasyID3)
    print ("%s Metadata parsing:" % color('[+]','OKBLUE'))

    # Song title
    mp3file['title'] = song
    mp3file.save()
    print ("\t%s Title parsed: " % color('[+]','OKGREEN') + mp3file['title'][0])

    # Artist
    mp3file['artist'] = artist
    mp3file.save()
    print ("\t%s Artist parsed: " % color('[+]','OKGREEN') + mp3file['artist'][0])

    # Album
    if album == "":
        for i, j in enumerate(googled):
            if "Album:" in j:
                album = (googled[i + 1])
    try:
        mp3file['album'] = album
        print ("\t%s Album parsed: " % color('[+]','OKGREEN') + mp3file['album'][0])
    except Exception:
        mp3file['album'] = album
        print ("\t%s Album not parsed" % color('[-]','FAIL'))
    mp3file.save()

    # Release date
    for i, j in enumerate(googled):
        if "Released:" in j:
            date = (googled[i + 1])
    try:
        mp3file['date'] = date
        print ("\t%s Release date parsed" % color('[+]','OKGREEN'))
    except Exception:
        mp3file['date'] = ""
    mp3file.save()

    # Track number
    if tracknum != "":
        mp3file['tracknumber'] = str(tracknum)
        mp3file.save()

    # Album art
    if mp3file['album'][0] != "":
        try:
            embed_mp3(get_albumart_url(album, artist), "%s/%s" % (location, filename))
            print ("\t%s Album art parsed" % color('[+]','OKGREEN'))
        except Exception as e:
            print ("\t%s Album art not parsed" % color('[-]','FAIL'))

    print ("\n%s \"%s\" downloaded successfully!\n" % (color('[+]','OKGREEN'), song))

def embed_mp3(albumart_url, song_location):
    img = urllib.request.urlopen(albumart_url)
    audio = mutagen.mp3.EasyMP3(song_location, ID3=mutagen.id3.ID3)
    try:
        audio.add_tags()
    except Exception as e:
        pass
    audio.tags.add(
        mutagen.id3.APIC(
            encoding = 3,  # UTF-8
            mime = 'image/png',
            type = 3,  # 3 is for album art
            desc = 'Cover',
            data = img.read()  # Reads and adds album art
        )
    )
    audio.save()

def get_albumart_url(album, artist):
    try:
        search = "%s %s" % (album, artist)
        url = "http://www.seekacover.com/cd/" + urllib.parse.quote_plus(search)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        done = False
        for img in soup.findAll('img'):
            if done == False:
                try:
                    if search.lower() in img['title'].lower():
                        return img['src']
                        done = True
                except Exception as e:
                    pass
    except Exception as e:
        pass
