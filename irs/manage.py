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

def find_mp3(song, artist,
    choose_link=False, # Whether to allow the user to choose the link.
        ):

    os.system("clear")
    print (color(song, ["BOLD", "UNDERLINE"]) + ' by ' + color(artist, ["BOLD", "UNDERLINE"]))

    search_terms = song + " " + artist + " lyrics"
    query_string = urlencode({"search_query" : (search_terms)})

    html_content = urlopen("http://www.youtube.com/results?" + query_string)
    search_results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

    in_title = False
    i = -1
    given_up_score = 0

    if not choose_link:
        print (bc.YELLOW + "\nFinding youtube link ...", end="\r")
        while in_title == False:
            i += 1
            given_up_score += 1

            if given_up_score >= 10:
                in_title = True

            audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
            title = strip_special_chars((BeautifulSoup(urlopen(audio_url), 'html.parser')).title.string.lower())
            song_title = song.lower().split("/")

            for song in song_title:
                song = strip_special_chars(song)
                if song in title and "full album" not in title:
                    in_title = True

        print (bc.OKGREEN + "Found youtube link!      \n" + bc.ENDC)
    else:
        results = []

        print (bc.YELLOW + "Finding links ... " + bc.ENDC, end="\r")

        for key in search_results[:10]:
            results.append(BeautifulSoup(urlopen(("http://www.youtube.com/watch?v="\
                + key)), 'html.parser').title.string.replace(" - YouTube" , ""))

        valid_choice = False
        while valid_choice == False:
            print (bc.HEADER + "What song would you like to download?")
            index = 0
            for result in results:
                index += 1
                print ("  %s) %s" % (index, result))
            i = int(input(bc.YELLOW + bc.BOLD + ":: " + bc.ENDC))
            if i in tuple(range(1, 11)):
                i -= 1
                valid_choice = True

    return search_results[i]

def rip_playlist(file_name,
    command=None, # Whether to run a special user-supplied command.
    choose_link=False, # Whether to allow the user to choose the link.
    no_organize=True, # Whether to organize the file downloaded.
        ):

    try:
        file = open(file_name, 'r')
    except Exception:
        print (file_name + bc.FAIL + " could not be found." + bc.ENDC)
        exit(1)

    errors = []

    song_number = 0

    for line in file:
        if line.strip() == "":
            pass

        try:
            arr = line.strip("\n").split(" - ")
            song = arr[0]
            artist = arr[1]

            if os.path.isdir(artist):
                remove = False
            else:
                remove = True

            location = rip_mp3(song, artist, command=command)

            song_number += 1

            locations = location.split("/")

            # Enter... the reorganizing...
            if no_organize:

                folder_name = ("playlist - " + file_name)[:40]

                if not os.path.isdir(folder_name):
                    os.makedirs(folder_name)

                os.rename(location, "%s/%s - %s" % (folder_name, song_number, locations[-1]))

                if remove:
                    import shutil # Only import this if I have to.
                    shutil.rmtree(locations[0])

                if os.path.isfile(filename):
                    os.rename(filename, folder_name + "/" + filename)

                os.rename(folder_name, folder_name.replace("playlist"))

        except Exception as e:
            errors.append(line + color(" : ", ["YELLOW"]) + bc.FAIL + str(e) + bc.ENDC)

    if len(errors) > 0:
        print (bc.FAIL + "Something was wrong with the formatting of the following lines:" + bc.ENDC)

        for i in errors:
            print ("\t%s" % i)


def rip_album(album, artist,
    tried=False, # for if it can't find the album the first time
    search="album", # ditto
    command=None, # For running a command with the song's location
    choose_link=False # Whether to allow the user to choose the link.
        ):

    if search in (None, False):
        search = "album"

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

        print (bc.YELLOW + "\nFinding album cover ... " + bc.ENDC, end="\r")
        album_art_url = get_albumart_url(album, artist)
        print (bc.OKGREEN + "Album cover found: " + bc.ENDC + album_art_url)

        for i, j in enumerate(songs):
            song = j
            print (color("\n%s/%s - " % (i + 1, len(songs)), ["UNDERLINE"]), end="")
            rip_mp3(j, artist, part_of_album=True, album=album, tracknum=i + 1, \
                album_art_url=album_art_url, command=command, choose_link=choose_link)

        if len(errors) > 0:
            for error in errors: print (error)
        else:
            print (bc.BOLD + bc.UNDERLINE + album + bc.ENDC + bc.OKGREEN + " downloaded successfully!\n")

    except Exception as e:
        if str(e) == "local variable 'indexed' referenced before assignment" or str(e) == 'list index out of range':
            if tried != True:
                print (bc.OKBLUE + "Trying to find album ..." + bc.ENDC)
                rip_album(album, artist, tried=True, search="", choose_link=choose_link)
            else:
                print (bc.FAIL + 'Could not find album "%s"' % album + bc.ENDC)
        else:
            errors.append(bc.FAIL + "There was a problem with downloading: " + bc.ENDC + song + "\n" + str(e))
            pass


def rip_mp3(song, artist,
    part_of_album=False, # neccessary for creating folders.
    album=None, # if you want to specify an album and save a bit of time.
    tracknum=None, # to specify the tracknumber in the album.
    album_art_url=None, # if you want to save a lot of time trying to find album cover.
    command=None, # For running a command with the song's location.
    choose_link=False, # Whether to allow the user to choose the link.
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

    if command:
        loc = location + "/" + filename
        os.system((command.replace("%(loc)s", '"%s"' % loc) + " &"))

    return (location + "/" + filename)
