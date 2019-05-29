from .list import SpotifyList

class Album(SpotifyList):
    """A class for downloading albums as a whole."""

    def _SpotifyList__find_it(self):
        album = self.spotify_searcher.find_album(
            self.list_title, 
            self.list_author
        )
        return album

    def _SpotifyList__set_organization(self, song_index, song):
        pass