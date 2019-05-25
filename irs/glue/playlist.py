import os

from .list import SpotifyList

class Playlist(SpotifyList):
    """A class for downloading albums as a whole.
    The majority of specs for methods can be found in the SpotifyList file"""

    def __init__(self, playlist_name, username, organization="single-folder"):
        """
        :param playlist_name: a string, the name of the playlist
        :param username: a string, the username of the creator of the playlist
        :param organization: a string, following options:
            "single-folder": All of the songs downloaded will be put into a
                single folder. root-music-dir>playlist-name
            "standard": All of the songs downloaded will be 
                organized by root-music-dir>artist>album
        """
        super(Playlist, self).__init__(playlist_name, username)
        self.organization = organization

    def _SpotifyList__find_it(self): 
        playlist = self.spotify_searcher.find_playlist(
            self.list_title, 
            self.list_author
        )
        return playlist

    def _SpotifyList__set_organization(self, song_index, song):
        if self.organization == "standard":
            song.set_standard_organization()
        elif self.organization == "single-folder":
            # reindex the file names in order to keep them in alphabetical order
            song.provide_new_file_name("{} - {}.mp3".format(
                song_index, song.tags["title"]
            ))
            song.provide_new_location(os.path.join(
                os.getcwd(), self.list_title
            ))