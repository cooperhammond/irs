# Powered by:
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
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
from .config import CONFIG

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

        if media == 1:
            self.args.song = color_input("Song you would like to download")
            self.args.artist = color_input("Name of artist")
            self.rip_mp3()

        elif media == 2:
            self.args.album = color_input("Album you would like to download")
            self.rip_spotify_list("album")

        elif media == 3:
            self.args.playlist = color_input("Playlist name to search for")

            self.rip_spotify_list("playlist")

    def find_mp3(self, song=None, artist=None):
        if not song:
            song = self.args.song

        if not artist:
            artist = self.args.artist

        print (color(song, ["BOLD", "UNDERLINE"]) + ' by ' + color(artist, ["BOLD", "UNDERLINE"]))

        search_terms = song + " " + artist + " " + CONFIG["additional_search_terms"]
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
                try:
                    audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
                except Exception:
                    print (bc.FAIL + "Could not find song." + bc.ENDC)
                    return False

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

    def get_album_art(self, artist, album, id=None):
        spotify = spotipy.Spotify()

        if id:
            album = spotify.album(id)
            return album["images"][0]["url"]

        results = spotify.search(q=artist + " " + album, type='album')
        items = results['albums']['items']
        if len(items) > 0:
            album = items[0]['images'][0]['url']
            return album

    def rip_spotify_list(self, type):

        if type == "playlist":
            search = self.args.playlist

        elif type == "album":
            search = self.args.album

        if self.args.artist:
            search += self.args.artist

        try:
            client_credentials_manager = SpotifyClientCredentials(CONFIG["client_id"], CONFIG["client_secret"])
            spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except spotipy.oauth2.SpotifyOauthError:
            spotify = spotipy.Spotify()

        if type == "user":
            items = spotify.user_playlists(self.args.user)["items"]
            length = None
        else:
            results = spotify.search(q=search, type=type)
            items = results[type + "s"]['items']
            length = 10

        songs = []

        if len(items) > 0:
            spotify_list = choose_from_spotify_list(items, length=length)

            list_type = spotify_list["type"]
            name = spotify_list["name"]
            if list_type != "playlist":
                spotify_list = eval("spotify.%s" % list_type)(spotify_list["uri"])
            else:
                try:
                    spotify_list = spotify.user_playlist(spotify_list["owner"]["id"], \
                    playlist_id=spotify_list["uri"], fields="tracks,next")
                except spotipy.client.SpotifyException:
                    fail_oauth()

            print (bc.YELLOW + "\nFetching tracks and their metadata: " + bc.ENDC)

            increment = 0

            for song in spotify_list["tracks"]["items"]:

                increment += 1
                list_size = increment / len(spotify_list["tracks"]["items"])
                drawProgressBar(list_size)

                if list_type == "playlist":
                    song = song["track"]

                artist = spotify.artist(song["artists"][0]["id"])


                if list_type == "playlist":
                    album = (spotify.track(song["uri"])["album"])
                else:
                    album = spotify_list

                songs.append({
                    "name": song["name"].split(" - ")[0],
                    "artist": artist["name"],
                    "album": album["name"],
                    "tracknum": increment,
                    "album_cover": album["images"][0]["url"]
                })

            print (bc.OKGREEN + "\nFound tracks:" + bc.ENDC)

            print (bc.HEADER)
            for song in songs:
                print ("\t" + song["name"] + " - " + song["artist"])
            print (bc.ENDC + "\n")

            if self.args.start_at:
                start_at = int(self.args.start_at) - 1
                if start_at < 0:
                    start_at = 0
            else:
                start_at = 0

            for song in songs[start_at:]:

                already_there = False
                if os.path.isdir(CONFIG["directory"] + "/" + song["artist"]):
                    already_there = True

                song_loc = self.rip_mp3(song["name"], song["artist"], album=song["album"], \
                tracknum=song["tracknum"], album_art_url=song["album_cover"], \
                out_of="%s/%s - " % (song["tracknum"], len(songs)))

                if song_loc == False:
                    continue

                if self.args.one_folder:

                    one_folder = CONFIG["directory"] + "/" + strip_special_chars(name[:30])

                    if not os.path.isdir(one_folder):
                        os.makedirs(one_folder)

                    new_loc = one_folder + "/" + song_loc.split("/")[-1]

                    os.rename(song_loc, new_loc)

                    if not already_there:
                        import shutil
                        shutil.rmtree(CONFIG["directory"] + "/" + song["artist"])

                    if self.args.command:
                        os.system((self.args.command.replace("%(loc)s", '"%s"' % new_loc) + " &"))


        else:
            print (bc.FAIL + "No results were found. Make sure to use proper spelling and capitalization." + bc.ENDC)
            exit(1)

    def rip_mp3(self, song=None, artist=None,
        album=None, # if you want to specify an album and save a bit of time.
        tracknum=None, # to specify the tracknumber in the album.
        album_art_url=None, # if you want to save a lot of time trying to find album cover.
        out_of="", # For a string to put before the song title.
            ):


        if not song:
            song = self.args.song

        if not artist:
            artist = self.args.artist


        print (color(out_of, ["UNDERLINE"]), end="")
        audio_code = self.find_mp3(song=song, artist=artist)

        if audio_code == False:
            return False

        if CONFIG["numbered_file_names"] and tracknum:
            track = str(tracknum) + " - "
        else:
            track = ""

        filename = track + strip_special_chars(song) + ".mp3"

        if CONFIG["download_file_names"]:
            filename = track + strip_special_chars((BeautifulSoup(\
            urlopen("http://www.youtube.com/watch?v=" + audio_code), 'html.parser'))\
            .title.string.lower()).strip("youtube") + ".mp3"

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


        artist_folder = CONFIG["directory"] + "/" + artist

        if not os.path.isdir(artist_folder):
            os.makedirs(artist_folder)

        if album:
            album_folder = CONFIG["directory"] + "/" + artist + "/" + album
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

        try:
            image_url = mp3.add_album_art(self.get_album_art(artist, mp3.get_attr('album')))
            exclaim_good("Album art: ", image_url)
        except Exception:
            print (bc.FAIL + "Album art not added." + bc.ENDC)


        print (color(song, ["BOLD", "UNDERLINE"]) + bc.OKGREEN + ' downloaded successfully!'+ bc.ENDC)
        print ("")

        if self.args.command:
            loc = location + "/" + filename
            os.system((self.args.command.replace("%(loc)s", '"%s"' % loc) + " &"))

        return (location + "/" + filename)
