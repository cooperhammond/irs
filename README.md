# Ironic Redistribution System
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](http://www.gnu.org/licenses/gpl.html)
[![PyPI](https://img.shields.io/badge/PyPi-Python_3.x-blue.svg)](https://pypi.python.org/pypi/irs)

<em>Spotify playlists are now downloadable!</em>

An ironically named program to download audio from youtube and then parse metadata for the downloaded file.
___
### Usage and Examples
To download Spotify playlists, you need to supply client_ids. To do this, you'll want to create an application [here](https://developer.spotify.com/my-applications/#!/applications/create). Once you've done that, you'll want to copy your 'client id' and your 'client secret' into the config file and their corresponding lines. To find the config file run this command: `irs -C`. If that's all working, enter the name of the playlist you would like to download like this:
```bash
irs -p "Brain Food"
```
If you download a specific song, you'll want to use the `-s` and `-a` flag.
```bash
irs -a "David Bowie" -s "Ziggy Stardust"
```
To download an entire album, you'll want to use the `-A` flag. If the album you want can't be found, run it with the `-a` flag for some more specification.
```bash
irs -A "Sadnecessary" # -a "Milky Chance"
```
[![asciicast](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug.png)](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug?speed=3&autoplay=true)

[![asciicast](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia.png)](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia?speed=3)

Full usage:
```
usage:
    irs (-h | -v)
    irs [-l]
    irs -p PLAYLIST [-c COMMAND] [-l]
    irs -A ALBUM [-c COMMAND] [-l]
    irs -a ARTIST -s SONG [-c COMMAND] [-l]

Options:
  -h, --help            show this help message and exit
  -v, --version         Display the version and exit.
  -A ALBUM, --album ALBUM
                        Search spotify for an album.
  -p PLAYLIST, --playlist PLAYLIST
                        Search spotify for a playlist.
  -c COMMAND, --command COMMAND
                        Run a background command with each song's location.
                        Example: `-c "rhythmbox %(loc)s"`
  -a ARTIST, --artist ARTIST
                        Specify the artist name. Only needed for -s/--song
  -s SONG, --song SONG  Specify song name of the artist. Must be used with
                        -a/--artist
  -l, --choose-link     If supplied, will bring up a console choice for what
                        link you want to download based off a list of titles.
```
Make a note that capitalization and spelling matters a lot in this program.

___
### Installation
Please note that it currently is only usable in `Python 3.x`. Almost all dependencies are automatically installed by pip, but `youtube_dl` still needs `ffmpeg` to convert video to audio, so for Windows, you can install [`Scoop`](http://scoop.sh/) and then just do:
```
scoop install ffmpeg
```
For OSX, you can use [`Brew`](http://brew.sh/) to install `ffmpeg`:
```
brew install ffmpeg
```
And then for Ubuntu:
```
sudo apt-get install ffmpeg
```
Most other linux distros have `ffmpeg` or `libav-tools` in their package manager repos, so you can install one or the other for other distros.

Finally, install it!
```
pip install irs
```

### Why the name?
As an acronym, it spells IRS. I think this is breathtakingly hilarious because the Internal Revenue Service (also the IRS) takes away, while my program gives. I'm so funny. You can tell that I'll get laid in college.


### Wishlist
 - [x] Finds album based off of song name and artist
 - [x] Full album downloading
 - [x] Album art metadata correctly displayed
 - [x] Playlist downloading
 - [x] Spotify playlist downloading
 - [ ] GUI/Console interactive version - <em>In progress</em>
 - [ ] 100% success rate for automatic song choosing
