# Ironic Redistribution System

[![License: GNU](https://img.shields.io/badge/license-gnu-yellow.svg?style=flat-square)](http://www.gnu.org/licenses/gpl.html)
[![Stars](https://img.shields.io/github/stars/kepoorhampond/irs.svg?style=flat-square)](https://github.com/kepoorhampond/irs/stargazers)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg?style=flat-square)](https://saythanks.io/to/kepoorhampond)
[![PyPI](https://img.shields.io/badge/pypi-irs-blue.svg?style=flat-square)](https://pypi.python.org/pypi/irs)

> A music downloader that understands your metadata needs.

A tool to download your music with metadata. It uses [Spotify](https://www.spotify.com/) for finding metadata and [Youtube](https://www.youtube.com/) for the actual audio source. You will need to have some Spotify tokens, the instructions to set them up are [here](https://github.com/kepoorhampond/irs#spotify-tokens).

Works with Python 2 and 3.

## Install and Setup
```
$ sudo pip install irs
$ irs --setup
```

**You will need to have some Spotify tokens, the instructions to set them up are [here](https://github.com/kepoorhampond/irs#spotify-tokens).**


## Demo and Usages

The usages can be found with the `-h` or `--help` flag:
```
usage: irs [-h] [-S] [-a ARTIST] [-s SONG] [-A ALBUM] [-p PLAYLIST]
           [-u USERNAME] [-o ORGANIZATION]

optional arguments:
  -h, --help            show this help message and exit
  -S, --setup           Run this by itself to setup config files and folder
                        for irs and download the ffmpeg binaries
  -a ARTIST, --artist ARTIST
                        Specify artist name. Must be used with -s/--song or
                        -A/--album
  -s SONG, --song SONG  Specify song name. Must be used with -a/--artist
  -A ALBUM, --album ALBUM
                        Specify album name. Can be used by itself.
  -p PLAYLIST, --playlist PLAYLIST
                        Specify playlist name. Must be used with -A/--album
  -u USERNAME, --username USERNAME
                        Specify user name for playlist. Must be used with
                        -A/--album
  -o ORGANIZATION, --organization ORGANIZATION
                        Specify type of organization for list. Used when
                        downloading spotify playlist/album
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

## Spotify Tokens

To download metadata through spotify, you'll want to head to their Dev Apps page, [here](https://developer.spotify.com/my-applications/). After doing that you'll want to create a new app. Name it whatever you want and then once you've done that, find the `Client ID` and `Client Secret` keys. You'll want to take those keys and paste them into your system's environment variables as `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`, correspondingly. Voilà! You can now download metadata with IRS!

## Metadata

Currently, the program attaches the following metadata to the downloaded files:
 - Title
 - Artist
 - Album
 - Album Art
 - Genre
 - Track Number
 - Disc Number

## Wishlist

 - [x] Full album downloading
 - [x] Album art metadata correctly displayed
 - [x] Spotify playlist downloading
 - [ ] Comment metadata
 - [ ] Compilation metadata
 - [ ] GUI/Console interactive version - *in progress*
 - [ ] Lyric metadata
