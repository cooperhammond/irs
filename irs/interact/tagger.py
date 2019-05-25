import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlopen
elif sys.version_info[0] < 3:
    from urllib import quote_plus, quote
    from urllib import urlopen

from mutagen.mp3 import EasyMP3
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.id3 import APIC, ID3


class Tagger(object):
    """Attaches ID3 tags to MP3 files."""

    def __init__(self, location):
        """Initializes the class and generates ID3 tags for the mp3
        :param location: a string, the location of the mp3 that you want ID3 
            tags on
        """
        EasyID3.RegisterTextKey("comment", "COMM")
        self.location = location
        self.mp3 = EasyID3(self.location)

    def add_tag(self, tag, data):
        """Adds a tag to the mp3 file you specified in __init__ and saves it
        :param tag: a string, the name of the tag you want to add to the mp3
            valid tag names:
                "title", "artist", "album", "genre", "tracknumber" (string), 
                "discnumber" (string), 
                "compilation" ("1" for true, "" for false)
        :param data: a string, the data that you want to attach to the mp3
            under the specified tag name
        """
        # For valid tags: `EasyID3.valid_keys.keys()`
        self.mp3[tag] = data
        self.mp3.save()

    def read_tag(self, tag):
        """Tries to read a tag from the initialized mp3 file
        :param tag: a string, the name of the tag you want to read
        :rtype: an array with a string inside. The string inside the array is
            the data you're requesting. If there's no tag associated or no data
            attached with your requested tag, a blank array will be returned. 
        """
        try:
            return self.mp3[tag]
        except EasyID3KeyError or KeyError:
            return []

    def add_album_art(self, image_url):
        """Adds album art to the initialized mp3 file
        :param image_url: a string, the url of the image you want to attach to
            the mp3
        """
        mp3 = EasyMP3(self.location, ID3=ID3)
        mp3.tags.add(
            APIC(
                encoding = 3,
                mime     = 'image/png',
                type     = 3,
                desc     = 'cover',
                data     = urlopen(image_url).read()
            )
        )
        mp3.save()