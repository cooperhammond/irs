import abc

from ..search import spotify
from .song import Song

class SpotifyList(object):
    """A parent class for downloading spotify albums and playlists"""

    def __init__(self, list_title, list_author=None):
        self.spotify_searcher = spotify.SpotifySearcher().authorize()
        self.list_title = list_title
        self.list_author = list_author
        self.file_names = []

    def grab_it(self):
        """Downloads the songs!
        """
        spotify_list = self.__find_it()
        list_contents = spotify_list["tracks"]["items"]

        for index, s in enumerate(list_contents):
            # if it's a playlist, get the actual track, not the metadata of 
            # the playlist
            if s.get("track"): 
                s = s["track"]
            
            song = Song(s["name"], s["artists"][0]["name"])
            song.provide_spotify(self.spotify_searcher)
            song.provide_metadata(self.spotify_searcher.song(s["uri"]))
            song.get_relevant_tags()
            self.__set_organization(index, song)
            song.grab_it()

    # These following functions are named weird b/c PEP8 and python are in 
    # conflict. An error gets raised when private methods 
    # (prefix = __ due to PEP8) are overriden by child class with the same 
    # name b/c python is dumb with how it concatenates class names and method
    # names with underscores

    def __find_it(self):
        """Finds the list and return it"""
        raise NotImplementedError("Must override __find_it with"
            "_SpotifyList__find_it")

    def __set_organization(self, song_index, song):
        """Post processing method for a single song
        :param song: Song class
        """
        raise NotImplementedError("Must override __post_process with"
            "_SpotifyList__set_organization")