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
            spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            self.authorized = True
        except spotipy.oauth2.SpotifyOauthError:
            spotify = spotipy.Spotify()
            self.authorized = False
            
    def find_yt_url(self, song=None, artist=None, additional_search="lyrics"):
        if not song:
            song = self.args["song"]
        
        if not artist:
            artist = self.args["artist"]
            
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
    