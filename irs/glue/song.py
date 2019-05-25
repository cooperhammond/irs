import os
import errno
import string

from ..search import spotify, youtube
from ..interact import ripper, tagger


class Song(object):
    """A grabber for a single song. Unless provided, gets metadata, finds url,
        downloads, converts, tags, and moves it."""
    def __init__(self, song_title, artist_name):
        self.song_title = song_title
        self.artist_name = artist_name

        self.spotify_searcher = None
        self.spotify_authenticated = False

        self.metadata = None
        self.tags = {}
        self.parsed_tags = False

        self.file_name = song_title + ".mp3"
        self.end_file_name = None

        self.current_location = os.getcwd()
        self.end_location = None

    def grab_it(self, post_process=True):
        """The main method to call for this class. Unless provided, grabs 
            metadata, finds the url, downloads the video, converts it, and 
            tags it.
        :param post_process: boolean, 
        :rtype: a string, the file_name
        """

        self.metadata = self.__parse_data()

        self.tags = self.get_relevant_tags()

        print("Searching youtube ...")
        song_url = youtube.find_url(self.tags["title"], self.tags["artist"])

        if self.metadata:
            self.file_name = '{} - {}.mp3'.format(
                self.tags["tracknumber"], 
                self.tags["title"]
            )

        print("Downloading ...")
        ripper.rip_from_url(song_url, self.file_name)
        print("Converting to mp3 ...") # TODO: add this into a hook for ydl

        print("Tagging ...")
        song_tags = tagger.Tagger(self.file_name)

        for tag in self.tags:
            if tag is "albumart":
                song_tags.add_album_art(self.tags[tag])
            else:
                song_tags.add_tag(tag, self.tags[tag])

        if post_process:
            self.__organize()

    def provide_spotify(self, spotify_searcher):
        """This function will set this class's spotify searcher to the one 
            provided to prevent the need to authenticate twice
        :param spotify_searcher: an instance of 
            irs.searcher.spotify.SpotifySearcher, the spotify searcher to use
        :rtype: self class
        """
        self.spotify_searcher = spotify_searcher
        self.spotify_authenticated = True
        return self

    def provide_metadata(self, metadata):
        """Provides metadata for the song so searches don't have to be 
            performed twice. If this is called with new metadata, 
            other metadata won't be searched.
        :param metadata: a dict, the new metadata from a spotipy track search
        :rtype: self class
        """
        self.metadata = metadata
        return self

    def provide_tag(self, key, value):
        """Provides tags for the song. Tags will still be parsed, but will not
            overwrite these provided tags.
        :param: a dict, the tags that will overwrite the metadata provided tags
        :rtype: self class
        """
        self.tags[key] = value
        return self

    def provide_new_location(self, new_loc):
        """Provides a new, non-default location for the song.
        :param new_loc: a string, the path of the new location WITHOUT filename
        :rtype: self class
        """
        self.end_location = new_loc
        return self

    def provide_new_file_name(self, new_name):
        """Provides a new file name for the song file. DOESNT append .mp3
        :param new_name: string
        :rtype: self class
        """
        self.end_file_name = new_name
        return self

    def set_standard_organization(self):
        """Sets standard organization for the file, which is
        root-music-dir>artist-folder>album-folder>song
        """
        if not self.parsed_tags:
            self.tags = self.get_relevant_tags()
        self.end_location = os.path.join(
            os.environ.get("irs_music_dir"), self.tags["artist"],
            self.tags["album"]
        )
        self.end_file_name = "{} - {}.mp3".format(
            self.tags["tracknumber"], self.tags["title"]
        )

    def get_relevant_tags(self):
        """Sorts relevant info from the spotipy metadata. Merges with any 
            provided tags from provide_tags method.
        :rtype: a dict, parsed tags
        """
        # TODO: come up with fallback solution if there's no metadata found
        # follows this pattern:
        # if this does not exist:
        #   set the thing that doesn't exist to a
        #   specific value from the metadata dict
        tags = self.tags
        metadata = self.metadata

        if not tags.get("title"):
            tags["title"] = metadata["name"]
        if not tags.get("artist"):
            tags["artist"] = metadata["artists"][0]["name"]
        if not tags.get("album"):
            tags["album"] = metadata["album"]["name"]
        if not tags.get("tracknumber"):
            tags["tracknumber"] = str(metadata["track_number"])
        if not tags.get("albumart"):
            tags["albumart"] = metadata["album"]["images"][0]["url"]
        if not tags.get("genre") and self.spotify_searcher:
            tags["genre"] = string.capwords(self.spotify_searcher.artist(
                metadata["artists"][0]["uri"])["genres"][0])

        self.tags = tags
        return self.tags

    def __organize(self):
        """Based off of self.current_location, self.end_location, and self.
        file_name, this function creates folders for the end location and moves
        the file there.
        """
        if not self.end_location:
            self.set_standard_organization()

        if not os.path.exists(self.end_location):
            # try loop to prevent against race conditions with os.path.exists
            # and os.makedirs 
            try:
                os.makedirs(self.end_location)
            except OSError as exc: 
                if exc.errno != errno.EEXIST:
                    raise

        os.rename(
            self.current_location + "/" + self.file_name,
            self.end_location + "/" + self.end_file_name,
        )

    def __parse_data(self):
        """If a spotify searcher has not been provided, create one."""
        if not self.spotify_authenticated and not self.metadata:
            self.spotify_searcher = spotify.SpotifySearcher().authorize()
            self.spotify_authenticated = True

        """If metadata has not been provided, search for it."""
        if not self.metadata:
            print("Searching for metadata ...")
            self.metadata = self.spotify_searcher.find_song(
                self.song_title, self.artist_name
            )

        return self.metadata        
