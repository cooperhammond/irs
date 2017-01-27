# Ironic Redistribution System
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](http://www.gnu.org/licenses/gpl.html)
[![PyPI](https://img.shields.io/badge/PyPi-Python_3.x-blue.svg)](https://pypi.python.org/pypi/irs)

<em>Spotify playlists are now downloadable! Just use the `-u` flag and your username!</em>

An ironically named program to download audio from youtube and then parse metadata for the downloaded file.
___
### Usage and Examples
For a non-descript Spotify playlist:
```bash
irs -p "Brain Food"
```
If you are looking for one of *your* playlists, you'll want to use the `-u` flag and put your username in:
```bash
irs -u "prakkillian"
```
If you download a specific song, you'll want to use the `-s` and `-a` flag.
```bash
irs -a "David Bowie" -s "Ziggy Stardust"
```
To download an entire album, you'll want to use the `-A` flag. If the album you want can't be found, run it with the `-a` flag for some more specification.
```bash
irs -A "Sadnecessary" # -a "Milky Chance"
```
[![asciicast](https://asciinema.org/a/5aijmkdux6nk8ckhke0jmzlyq.png)](https://asciinema.org/a/5aijmkdux6nk8ckhke0jmzlyq?speed=3&autoplay=true)

[![asciicast](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia.png)](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia?speed=3)

Full usage:
```
usage:
    irs (-h | -v | -C)
    irs [-l] [-sa]
    irs -p PLAYLIST [-c COMMAND] [-l] [-sa]
    irs -A ALBUM [-c COMMAND] [-l] [-sa]
    irs -a ARTIST -s SONG [-c COMMAND] [-l]

Options:
  -h, --help            show this help message and exit
  -v, --version         Display the version and exit.
  -C, --config          Return location of configuration file.
  -A ALBUM, --album ALBUM
                        Search spotify for an album.
  -p PLAYLIST, --playlist PLAYLIST
                        Search spotify for a playlist.
  -u USER, --user USER  Download a user playlist.
  -c COMMAND, --command COMMAND
                        Run a background command with each song's location.
                        Example: `-c "rhythmbox %(loc)s"`
  -a ARTIST, --artist ARTIST
                        Specify the artist name. Only needed for -s/--song
  -s SONG, --song SONG  Specify song name of the artist. Must be used with
                        -a/--artist
  -l, --choose-link     If supplied, will bring up a console choice for what
                        link you want to download based off a list of titles.
  -sa, --start-at       A song index to start at if something goes wrong while
                        downloading and you have to restart.
```
Make a note that capitalization and spelling matters a lot in this program.

___
### Installation
To download Spotify playlists, you need to supply client_ids. To do this, you'll want to create an application [here](https://developer.spotify.com/my-applications/#!/applications/create). Once you've done that, you'll want to copy your 'client id' and your 'client secret' into the config file and their corresponding lines. To find the config file run this command: `irs -C`.

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
As an acronym, it spells IRS. I think this is breathtakingly hilarious because the Internal Revenue Service (also the IRS) takes away, while my program gives. I'm so funny.


### Wishlist
 - [x] Finds album based off of song name and artist
 - [x] Full album downloading
 - [x] Album art metadata correctly displayed
 - [x] Playlist downloading
 - [x] Spotify playlist downloading
 - [ ] GUI/Console interactive version - <em>In progress</em>
 - [ ] 100% success rate for automatic song choosing
