import urllib.request, urllib.parse, re, sys, os, requests
import youtube_dl
from bs4 import BeautifulSoup
from .utils import *
from .metadata import *

def find_mp3(song, artist):
    search_terms = song + " " + artist
    print ("\"%s\" by %s" % (song, artist))
    query_string = urllib.parse.urlencode({"search_query" : (search_terms)})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    in_title = False
    i = -1
    given_up_score = 0
    while in_title == False:
        i += 1
        given_up_score += 1
        if given_up_score >= 10:
            in_title = True
        audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
        title = strip_special_chars((BeautifulSoup(urllib.request.urlopen(audio_url), 'html.parser')).title.string.lower())
        song_title = song.lower().split("/")
        for song in song_title:
            if strip_special_chars(song) in strip_special_chars(title):
                in_title = True
    return search_results[i]

def rip_album(album, artist, tried=False, search="album"):
    visible_texts = search_google(album, artist, search)
    try:
        songs = []
        num = True
        for i, j in enumerate(visible_texts):
            if 'Songs' in j:
                if visible_texts[i + 1] == "1":
                    indexed = i
        while num == True:
            try:
                if type(int(visible_texts[indexed])) is int:
                    a = visible_texts[indexed + 1]
                    songs.append(a)
                    indexed += 1
            except:
                indexed += 1
                if indexed >= 1000:
                    num = False
                else:
                    pass

        for i, j in enumerate(songs):
            rip_mp3(j, artist, part_of_album=True, album=album, tracknum=i + 1)

    except Exception as e:
        if str(e) == "local variable 'indexed' referenced before assignment" or str(e) == 'list index out of range':
            if tried != True:
                print ("%s Trying to find album ..." % color('[*]','OKBLUE'))
                rip_album(album, artist, tried=True, search="")
            else:
                print ("%s Could not find album '%s'" % (color('[-]','FAIL'), album))
        else:
            print ("%s There was an error with getting the contents \
of the album '%s'" % (color('[-]','FAIL'), album))

def rip_mp3(song, artist, part_of_album=False, album="", tracknum=""):
    audio_code = find_mp3(song, artist)
    filename = strip_special_chars(song) + ".mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        #'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["http://www.youtube.com/watch?v=" + audio_code])

    artist_folder = artist
    if not os.path.isdir(artist_folder):
        os.makedirs(artist_folder)
    if not part_of_album:
        location = artist_folder

    if album != "" and part_of_album:
        album_folder = artist + "/" + album
        if not os.path.isdir(album_folder):
            os.makedirs(album_folder)
        location = album_folder

    for file in os.listdir("."):
        if audio_code in file:
            os.rename(file, location + "/" + filename)

    parse_metadata(song, artist, location, filename, tracknum=tracknum, album=album)
