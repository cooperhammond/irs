<div style="text-align:center">![](http://i.imgur.com/VbsyTe7.png)</div>

Ironic Redistribution System
===
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](http://www.gnu.org/licenses/gpl.html)
[![Stars](https://img.shields.io/github/stars/kepoorhampond/irs.svg)](https://github.com/kepoorhampond/irs/stargazers)
[![PyPI](https://img.shields.io/badge/PyPi-irs-blue.svg)](https://pypi.python.org/pypi/irs)

> A music downloader that understands your metadata needs.

A tool to download your music with metadata. It uses [Spotify](https://www.spotify.com/) for finding metadata and list contents and uses [Youtube](https://www.youtube.com/) for the actual audio.

Works with Python 2 and 3.
___
Demo and Usages
---
This is a demo of the CLI displayling its features:
[![demo](https://asciinema.org/a/105993.png)](https://asciinema.org/a/105993?autoplay=1)

The usages can be found with the `-h` or `--help` flag:
```
usage: irs [-h] [(-a ARTIST -s SONG)] [-A ALBUM] [(-u USERNAME -p PLAYLIST)]

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Specify artist name. Must be used with -s/--song
  -s SONG, --song SONG  Specify song name. Must be used with -a/--artist
  -A ALBUM, --album ALBUM
                        Specify album name
  -u USERNAME, --username USERNAME
                        Specify username. Must be used with -p/--playlist
  -p PLAYLIST, --playlist PLAYLIST
                        Specify playlist name. Must be used with -u/--username
```
So all of these are valid commands:
```
$ irs -a "Brandon Flowers" -s "Lonely Town"
$ irs -u "spotify" -p "Brain Food"
$ irs -A "Suicide Squad: The Album"
```
But these are not:
```
$ irs -s "Bohemian Rhapsody"
$ irs -p "Best Nirvana"
```

Metadata
---
Currently, the program attaches the following metadata to the downloaded files:
 - Title
 - Artist
 - Album
 - Album Art
 - Genre
 - Track Number
 - Disc Number
 - Compilation (iTunes only)

### Philosophy
When I made this program I was pretty much broke and my music addiction wasn't really helping that problem. So, I did the obvious thing: make an uber-complicated program to ~~steal~~ download music for me! As for the name, its acronym spells IRS, which I found amusing, seeing as the IRS ~~takes~~ steals money while my program ~~gives~~ reimburses you with music.

### Wishlist
 - [x] Finds album based off of song name and artist
 - [x] Full album downloading
 - [x] Album art metadata correctly displayed
 - [x] Spotify playlist downloading
 - [ ] GUI/Console interactive version - *in progress*
 - [ ] Lyric metadata
 - [ ] 99% success rate for automatic song choosing

