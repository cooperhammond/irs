# Ingenious Redistribution System
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](http://www.gnu.org/licenses/gpl.html)
[![PyPI](https://img.shields.io/badge/PyPi-Python_3.5-blue.svg)](https://pypi.python.org/pypi/irs)

<em>Now with working album art!</em>

An ingenious program to download audio from youtube and then parse metadata for the downloaded file.
___
### Usage and Examples
```
usage: irs [-h] [-a ARTIST] [-A ALBUM | -s SONG]

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Specify the artist name
  -A ALBUM, --album ALBUM
                        Specify album name of the artist
  -s SONG, --song SONG  Specify song name of the artist
```
[![asciicast](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug.png)](https://asciinema.org/a/bcs7i0sjmka052wsdyxg5xrug?speed=3&autoplay=true)
___
### Installation
```
$ pip install irs
```
Almost all dependencies are automatically installed by pip, but youtube_dl still needs ffmpeg to convert video to audio, so for Windows, you can install [`Scoop`](http://scoop.sh/) and then just do:
```
$ scoop install ffmpeg
```
For OSX, you can use [`Brew`](http://brew.sh/) and do:
```
$ brew install ffmpeg
```
For Ubuntu:
```
$ sudo apt-get install ffmpeg
```
<sub><sup>Most other linux distros have `ffmpeg` or `libav-tools` in their package manager repos, so you can install one or the other for other distros.<sup><sub>