import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = 'e4198f6a3f7b48029366f22528b5dc66'
CLIENT_SECRET = 'ba057d0621a5496bbb64edccf758bde5'


class SpotifySearcher(object):
    """Searches spotify for song, album, and playlist metadata."""

    def authorize(self, client_id=None, client_secret=None):
        """Authorizes this class with spotify using client ids
        :rtype: returns self class
        """

        # TODO: remove these when you finish config files
        if not client_id:
            client_id = 'e4198f6a3f7b48029366f22528b5dc66'
        if not client_secret:
            client_secret = 'ba057d0621a5496bbb64edccf758bde5'

        try:
            creds = SpotifyClientCredentials(client_id, client_secret)
            self.authorized = True
            self.spotify = spotipy.Spotify(client_credentials_manager=creds)
        except Exception:
            self.authorized = False
            self.spotify = spotipy.Spotify()

        return self

    def find_song(self, song_title, artist_name, limit=50, offset=0):
        """Searches spotify for a song and grabs its metadata
        :param song_title: a string, the title of the song you're looking for
        :param artist_name: a string, the artist of the above song
        :rtype: a dictionary of metadata about the song
        """
        songs = self.spotify.search(q=song_title, type="track")["tracks"]

        for song in songs["items"]:
            if _simplify(song_title) in _simplify(song["name"]) and \
               _simplify(artist_name) in _simplify(song["artists"][0]["name"]):
                return song
        
        if songs['next']:
            return self.find_song(song_title, artist_name, 
                offset=offset + limit)
        else:
            print("There were no songs found by that name with that artist")

    def find_album(self, album_title, artist_name=None, limit=50, offset=0):
        """Searches spotify for an album and grabs its contents and metadata
        :param album_title: a string, the title of the album
        :param artist_name: a string, the name of the artist of the album
        :rtype: a dictionary of metadata about the album
        """
        query = album_title
        if artist_name:
            query += " " + artist_name
        albums = self.spotify.search(q=query, type="album")['albums']

        for album in albums['items']:
            if _simplify(album_title) in _simplify(album["name"]):
                return self.spotify.album(album['uri'])

        if albums['next']:
            return self.find_album(album_title, artist_name, 
                offset=offset + limit)
        else:
            print("There were no albums found by that name with that artist")

    def find_playlist(self, playlist_title, username, limit=50, offset=0):
        """Searches spotify for a playlist and grabs its contents and metadata
        :param playlist_title: a string, the title of the playlist
        :param username: a string, the username of the playlist creator/owner
        :rtype: a dictionary of metadata about the playlist
        """
        playlists = []
        playlists = self.spotify.user_playlists(username, limit, offset)

        for playlist in playlists['items']:
            if _simplify(playlist_title) in _simplify(playlist['name']):
                return self.spotify.user_playlist(username, playlist['id'])

        if playlists['next']:
            return self.find_playlist(playlist_title, username, 
                offset=offset + limit)
        else:
            print("There were no playlists by that name found.")

    def artist(self, artist_uri):
        """Gets artist metadata from uri
        :param artist_uri: the spotify uri for the artist
        :rtype: a dict of info about the artist
        """
        return self.spotify.artist(artist_uri)

    def song(self, song_uri):
        """Gets song metadata from uri
        :param song_uri: the spotify uri for the artist
        :rtype: a dict of info about the artist
        """
        return self.spotify.track(song_uri)



# TODO: export this function to a utilities file
def _simplify(string):
    """Lowercases and strips all non alphanumeric characters from the string
    :param string: a string to be modified
    :rtype: the modified string
    """
    if type(string) == bytes:
        string = string.decode()
    return re.sub(r'[^a-zA-Z0-9]+', '', string.lower())