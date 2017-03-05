# Powered by:
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# System
import sys
import os

# Parsing
from bs4 import BeautifulSoup
if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
elif sys.version_info[0] < 3:
    from urllib import urlencode
    from urllib import urlopen
else:
    print ("Must be using Python 2 or 3")
    sys.exit(1)
    
# Local utilities
import utils

class Ripper:
    def __init__(self, args={}):
        self.args = args
        self.locations = []
        try:
            client_credentials_manager = SpotifyClientCredentials(os.environ["SPOTIFY_CLIENT_ID"], os.environ["SPOTIFY_CLIENT_SECRET"])
            self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            self.authorized = True
        except spotipy.oauth2.SpotifyOauthError:
            self.spotify = spotipy.Spotify()
            self.authorized = False
            
    def find_yt_url(self, song=None, artist=None, additional_search="lyrics"):
        try:
            if not song:    song = self.args["song"]
            if not artist:  artist = self.args["artist"]
        except ValueError:
            raise ValueError("Must have specify `song` and/or `artist` in either init with `args` or with method arguments.")
            
        search_terms = song + " " + artist + " " + additional_search
        query_string = urlencode({"search_query" : (search_terms)})
        link = "http://www.youtube.com/results?" + query_string
        
        html_content = urlopen(link).read()
        soup = BeautifulSoup(html_content, 'html.parser')#.prettify
        
        def find_link(link):
            try:
                if "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link" in str(" ".join(link["class"])):
                    if not "&list=" in link["href"]: 
                        return link
            except KeyError:
                pass
                
        results = list(filter(None, (map(find_link, soup.find_all("a")))))
        
        garbage_phrases = "cover  album  live  clean  rare version".split("  ")
        
        self.code = None
        for link in results:
            if utils.blank_include(link["title"], song) and utils.blank_include(link["title"], artist):
                if utils.check_garbage_phrases: continue
                self.code = link
                break
                
        if self.code == None:
            for link in results:
                if utils.check_garbage_phrases: continue
                if utils.individual_word_match(song, link["title"]) >= 0.8 and utils.blank_include(link["title"], artist):
                    self.code = link
                    break
        
        if self.code == None:
            if additional_search == "lyrics":
                return self.find_yt_url(song, artist, "")
            else:
                self.code = results[0]
                
        return ("https://youtube.com" + self.code["href"], self.code["title"])
    
    def spotify_list(self, type=None, title=None, username=None):
        try:
            if not type:      type = self.args["type"]
            if not title:     title = self.args["title"]
            if not username:  username = self.args["username"] 
        except ValueError:
            raise ValueError("Must specify type/title/username in `args` with init, or in method arguements.")
        
        if type == "album":
            search = title
            if "artist" in self.args:
                search += " " + self.args["artist"]
            list_of_lists = self.spotify.search(q=search, type="album")
        elif type == "playlist":
            list_of_lists = self.spotify.user_playlists(username)
            
        if len(list_of_lists) > 0:
            the_list = None
            for list_ in list_of_lists:
                if utils.blank_include(list_.name, title):
                    if "artist" in self.args:
                        if utils.blank_include(list_["artists"][0]["name"], self.args["artist"]):
                            the_list = list_
                            break
                    else:
                        the_list = list_
                        break
            if the_list != None:
                print ('"%s" by "%s"' % (the_list["name"], the_list["artists"][0]["name"]))
                compilation = False
                if type == "album":
                    tmp_albums = []
                    tmp_artists = []
                    for track in the_list["tracks"]:
                        tmp_albums.append(track["album"]["name"])
                        tmp_artists.append(track["artists"][0]["name"])
                    tmp_albums = list(set(tmp_albums))
                    tmp_artists = list(set(tmp_artists))
                    if len(tmp_albums) == 1 and len(tmp_artists) > 1:
                        compilation = True
                
                tracks = []
                file_prefix = ""
                for track in the_list["tracks"]:
                    if type == "playlist": 
                        file_prefix = str(len(tracks)) + " - "
                    
                    data = {
                        "name":          track["name"],
                        "artist":        track["artists"][0]["name"],
                        "album":         track["album"],
                        "genre":         track["artists"][0]["genres"],
                        "track_number":  track["track_number"],
                        "disc_number":   track["disc_number"],
                        "compilation":   compilation,
                        "file_prefix":        file_prefix,
                    }
                    
                    tracks.append(data)
                
                locations = self.list(tracks)
                return self.post_processing(locations)
                
        print ('Could not find any lists.')
        return False

    def list(list_data):
        locations = []
        with open(".irs-download-log", "w+") as file:
            file.write(utils.format_download_log_data(list_data))
        
        for track in list_data:
            loc = self.song(track["name"], track["artist"], track)

            if loc != False:
                utils.update_download_log_line_status(track, "downloaded")
                locations.append(loc)
        
        os.remove(".irs-download-log")
        return locations