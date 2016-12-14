# Powered by:
import youtube_dl

# Info getting
from urllib.request import urlopen
from urllib.parse import urlencode

# Info parsing
from re import findall
import os, json
from bs4 import BeautifulSoup

# Local utils
from .utils import *
from .metadata import *

def find_mp3(song, artist):
    print (color(song, ["BOLD", "UNDERLINE"]) + ' by ' + color(artist, ["BOLD", "UNDERLINE"]) + '\n')

    search_terms = song + " " + artist
    query_string = urlencode({"search_query" : (search_terms)})

    html_content = urlopen("http://www.youtube.com/results?" + query_string)
    search_results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

    in_title = False
    i = -1
    given_up_score = 0

    while in_title == False:
        i += 1
        given_up_score += 1

        if given_up_score >= 10:
            in_title = True

        audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
        title = strip_special_chars((BeautifulSoup(urlopen(audio_url), 'html.parser')).title.string.lower())
        song_title = song.lower().split("/")

        for song in song_title:
            if strip_special_chars(song) in strip_special_chars(title):
                in_title = True

    return search_results[i]

def rip_album(album, artist,
    tried=False, # for if it can't find the album the first time
    search="album", # ditto
        ):
    visible_texts = search_google(album, artist, search)
    errors = []
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

        print ("")
        print (bc.HEADER + "Album Contents:" + bc.ENDC)
        for i, j in enumerate(songs):
            print (bc.OKBLUE + "  - " + j + bc.ENDC)

        print (bc.YELLOW + "\nFinding album cover ... " + bc.ENDC, end="")
        album_art_url = get_albumart_url(album, artist)
        print (bc.OKGREEN + "\rAlbum cover found: " + bc.ENDC + album_art_url)

        for i, j in enumerate(songs):
            song = j
            print (color("\n%s/%s - " % (i + 1, len(songs)), ["UNDERLINE"]), end="")
            rip_mp3(j, artist, part_of_album=True, album=album, tracknum=i + 1, album_art_url=album_art_url)

        if len(errors) > 0:
            for error in errors: print (error)

    except Exception as e:
        if str(e) == "local variable 'indexed' referenced before assignment" or str(e) == 'list index out of range':
            if tried != True:
                print (bc.OKBLUE + "Trying to find album ..." + bc.ENDC)
                rip_album(album, artist, tried=True, search="")
            else:
                print (bc.FAIL + 'Could not find album "%s"' % album + bc.ENDC)
        else:
            errors.append(bc.FAIL + "There was a problem with downloading: " + bc.ENDC + song)
            print (bc.FAIL + "Something major went wrong: " + str(e) + bc.ENDC)
            pass


def rip_mp3(song, artist,
    part_of_album=False, # neccessary for creating folders
    album=None, # if you want to specify an album and save a bit of time
    tracknum=None, # to specify the tracknumber in the album
    album_art_url=None # if you want to save a lot of time trying to find album cover.
        ):

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


    if album and part_of_album:
        album_folder = artist + "/" + album
        if not os.path.isdir(album_folder):
            os.makedirs(album_folder)
        location = album_folder


    for file in os.listdir("."):
        if audio_code in file:
            os.rename(file, location + "/" + filename)


    parse_metadata(song, artist, location, filename, tracknum=tracknum, album=album, album_art_url=album_art_url)


    print (color(song, ["BOLD", "UNDERLINE"]) + bc.OKGREEN + ' downloaded successfully!'+ bc.ENDC)
    print ("")
