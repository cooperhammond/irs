# Powered by:
import youtube_dl
import spotipy

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

class Manager:
    def __init__(self, args):
        self.args = args

    def console(self):

        args = self.args

        os.system("clear")
        media = None

        while type(media) is not int:
            print (bc.HEADER)
            print ("What type of media would you like to download?")
            print ("\t1) Song")
            print ("\t2) Album")
            print ("\t3) Playlist")
            try:
                media = int(input(bc.YELLOW + bc.BOLD + ":: " + bc.ENDC))
                if media not in (1, 2, 3):
                    raise ValueError

            except ValueError:
                print (bc.FAIL + "\nPlease enter a valid number." + bc.ENDC)

        if media in (1, 2):
            self.args.artist = color_input("Artist of song/album")

            if media == 1:
                self.args.song = color_input("Song you would like to download")
                self.rip_mp3()

            elif media == 2:
                self.args.album = color_input("Album you would like to download")
                self.rip_album()

        elif media == 3:
            self.args.playlist = color_input("Playlist file name")

            organize = ""
            while organize not in ("y", "n", "yes", "no", ""):
                print (bc.HEADER + "Would you like to place all songs into a single folder? (Y/n)", end="")
                organize = input(bc.BOLD + bc.YELLOW + ": " + bc.ENDC).lower()

            if organize in ("y", "yes", ""):
                self.args.organize = True
            elif organize in ("n", "no"):
                self.args.organize = False

            self.rip_playlist()

    def find_mp3(self, song=None, artist=None):
        if not song:
            song = self.args.song

        if not artist:
            artist = self.args.artist

        print (color(song, ["BOLD", "UNDERLINE"]) + ' by ' + color(artist, ["BOLD", "UNDERLINE"]))

        search_terms = song + " " + artist + " lyrics"
        query_string = urlencode({"search_query" : (search_terms)})

        html_content = urlopen("http://www.youtube.com/results?" + query_string)
        search_results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        in_title = False
        i = -1
        given_up_score = 0

        if not self.args.link:
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

            print (bc.YELLOW + "\nFinding links ... " + bc.ENDC, end="\r")

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


    def rip_playlist(self):
        file_name = self.args.playlist
        organize = self.args.organize

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

            #try:
            arr = line.strip("\n").split(" - ")
            self.args.song = arr[0]
            self.args.artist = arr[1]

            if os.path.isdir(self.args.artist):
                remove = False
            else:
                remove = True

            location = self.rip_mp3()
            locations = location.split("/")
            song_number += 1

            # Enter... the reorganizing...
            if organize:

                folder_name = ("playlist - " + file_name)[:40]

                if not os.path.isdir(folder_name):
                    os.makedirs(folder_name)

                os.rename(location, "%s/%s - %s" % (folder_name, song_number, locations[-1]))

                if remove:
                    import shutil # Only import this if I have to.
                    shutil.rmtree(locations[0])

        if organize:
            os.rename(file_name, folder_name + "/" + file_name)

            os.rename(folder_name, folder_name.replace("playlist - ", ""))

            #except Exception as e:
            #    errors.append(line + color(" : ", ["YELLOW"]) + bc.FAIL + str(e) + bc.ENDC)

        if len(errors) > 0:
            print (bc.FAIL + "Something was wrong with the formatting of the following lines:" + bc.ENDC)

            for i in errors:
                print ("\t%s" % i)

    def get_album_contents(self, search):
        spotify = spotipy.Spotify()

        results = spotify.search(q=search, type='album')
        items = results['albums']['items']
        if len(items) > 0:
            album = items[0]
            album_id = (album['uri'])
            contents = spotify.album_tracks(album_id)["items"]
            contents = contents[0:-1]
            names = []
            for song in contents:
                names.append(song["name"])
            return names

    def get_album_art(self, artist, album):
        spotify = spotipy.Spotify()

        results = spotify.search(q="album:" + album, type='album')
        items = results['albums']['items']
        if len(items) > 0:
            album = items[0]['images'][0]['url']
            return album


    def rip_album(self):
        search = self.args.artist + " " + self.args.album
        songs = self.get_album_contents(search)

        if not songs:
            print (bc.FAIL + "Could not find album." + bc.ENDC)
            exit(1)

        print ("")
        print (bc.HEADER + "Album Contents:" + bc.ENDC)
        for song in songs:
            print (bc.OKBLUE + "  - " + song + bc.ENDC)

        print (bc.YELLOW + "\nFinding album cover ... " + bc.ENDC, end="\r")
        album_art_url = self.get_album_art(self.args.artist, self.args.album)
        print (bc.OKGREEN + "Album cover found: " + bc.ENDC + album_art_url)

        for track_number, song in enumerate(songs):
            print (color("\n%s/%s - " % (track_number + 1, len(songs)), ["UNDERLINE"]), end="")
            self.rip_mp3(song, album=self.args.album, tracknum=track_number + 1, album_art_url=album_art_url)

        else:
            print (bc.BOLD + bc.UNDERLINE + self.args.album + bc.ENDC + bc.OKGREEN + " downloaded successfully!\n")


    def rip_mp3(self, song=None, artist=None,
        album=None, # if you want to specify an album and save a bit of time.
        tracknum=None, # to specify the tracknumber in the album.
        album_art_url=None, # if you want to save a lot of time trying to find album cover.
            ):

        if not song:
            song = self.args.song

        if not artist:
            artist = self.args.artist

        audio_code = self.find_mp3(song=song, artist=artist)

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

        if album:
            album_folder = artist + "/" + album
            if not os.path.isdir(album_folder):
                os.makedirs(album_folder)
            location = album_folder

        elif not album:
            location = artist_folder

        for file in os.listdir("."):
            if audio_code in file:
                os.rename(file, location + "/" + filename)


        # Metadata
        mp3 = Metadata(location + "/" + filename, song, artist)

        mp3.add_title()
        exclaim_good("Title added: ", song)

        mp3.add_artist()
        exclaim_good("Artist added: ", artist)

        test_goodness(mp3.add_album(album), "Album", "album", mp3)

        test_goodness(mp3.add_release_date(), "Release Date", "date", mp3)

        if tracknum:
            mp3.add_track_number(tracknum)

        image_url = mp3.add_album_art(self.get_album_art(artist, mp3.get_attr('album')))
        exclaim_good("Album art: ", image_url)


        print (color(song, ["BOLD", "UNDERLINE"]) + bc.OKGREEN + ' downloaded successfully!'+ bc.ENDC)
        print ("")

        if self.args.command:
            loc = location + "/" + filename
            os.system((self.args.command.replace("%(loc)s", '"%s"' % loc) + " &"))

        return (location + "/" + filename)
