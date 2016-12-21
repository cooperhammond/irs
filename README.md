# Ingenious Redistribution System
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](http://www.gnu.org/licenses/gpl.html)
[![PyPI](https://img.shields.io/badge/PyPi-Python_3.x-blue.svg)](https://pypi.python.org/pypi/irs)

<em>Now with working album art!</em>

An ingenious program to download audio from youtube and then parse metadata for the downloaded file.
___
### Usage and Examples
```
usage:
    irs (-h | -v)
    irs [-l]
    irs -p PLAYLIST [-ng] [-c COMMAND] [-l]
    irs -a ARTIST (-s SONG | -A ALBUM [-st SEARCH_TERMS]) [-c COMMAND] [-l]

Options:
  -h, --help            show this help message and exit
  -v, --version         Display the version and exit.
  -c COMMAND, --command COMMAND
                        Run a background command with each song's location.
                        Example: `-c "rhythmbox %(loc)s"`
  -a ARTIST, --artist ARTIST
                        Specify the artist name.
  -p PLAYLIST, --playlist PLAYLIST
                        Specify playlist filename. Each line in the file
                        should be formatted like so: `SONGNAME - ARTIST`
  -s SONG, --song SONG  Specify song name of the artist.
  -A ALBUM, --album ALBUM
                        Specify album name of the artist.
  -st SEARCH_TERMS, --search-terms SEARCH_TERMS
                        Only use if calling -A/--album. Acts as extra search
                        terms when looking for the album.
  -l, --choose-link     If supplied, will bring up a console choice for what
                        link you want to download based off a list of titles.
  -ng, --no-organize    Only use if calling -p/--playlist. Forces all files
                        downloaded to be organized normally.
```
[![asciicast](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug.png)](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug?speed=3&autoplay=true)

[![asciicast](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia.png)](https://asciinema.org/a/8kb9882j4cbtd4hwbsbb7h0ia?speed=3)

___
### Installation
Please note that it currently is only usable in `Python 3.x`. Almost all dependencies are automatically installed by pip, but `youtube_dl` still needs `ffmpeg` to convert video to audio, so for Windows, you can install [`Scoop`](http://scoop.sh/) and then just do:
```
$ scoop install ffmpeg
```
For OSX, you can use [`Brew`](http://brew.sh/) to install `ffmpeg`:
```
$ brew install ffmpeg
```
And then for Ubuntu:
```
$ sudo apt-get install ffmpeg
```
Most other linux distros have `ffmpeg` or `libav-tools` in their package manager repos, so you can install one or the other for other distros.

Finally, install it!
```
$ pip install irs
```
