<div align="center"><img src ="http://i.imgur.com/VbsyTe7.png" /></div>

# Ironic Redistribution System

[![License: GNU](https://img.shields.io/badge/license-gnu-yellow.svg?style=flat-square)](http://www.gnu.org/licenses/gpl.html)
[![Stars](https://img.shields.io/github/stars/kepoorhampond/irs.svg?style=flat-square)](https://github.com/kepoorhampond/irs/stargazers)
[![Build Status](https://img.shields.io/travis/kepoorhampond/irs/master.svg?style=flat-square)](https://travis-ci.org/kepoorhampond/irs)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg?style=flat-square)](https://saythanks.io/to/kepoorhampond)
[![PyPI](https://img.shields.io/badge/pypi-irs-blue.svg?style=flat-square)](https://pypi.python.org/pypi/irs)
[![Beerpay](https://beerpay.io/kepoorhampond/irs/badge.svg?style=flat-square)](https://beerpay.io/kepoorhampond/irs)

<sup><sub>(Shields: Gotta Catch Em All)</sub></sup>

> A music downloader that understands your metadata needs.

A tool to download your music with metadata. It uses [Spotify](https://www.spotify.com/) for finding metadata and [Youtube](https://www.youtube.com/) for the actual audio source. You will need to have some Spotify tokens, the instructions to set them up are [here](https://github.com/kepoorhampond/irs#spotify-tokens).

Works with Python 2 and 3.

## Install
```
$ sudo pip install irs
```

**You will need to have some Spotify tokens, the instructions to set them up are [here](https://github.com/kepoorhampond/irs#spotify-tokens).**

## Demo and Usages

This is a demo of the CLI displayling its features:
[![demo](https://asciinema.org/a/105993.png)](https://asciinema.org/a/105993?autoplay=1)

The usages can be found with the `-h` or `--help` flag:
```
usage: irs [-h] [-a ARTIST -s SONG] [-A ALBUM [-a ARTIST]]
           [-u USERNAME -p PLAYLIST] [-l LOCATION] [-o] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Specify artist name. Must be used with -s/--song or
                        -A/--album
  -s SONG, --song SONG  Specify song name. Must be used with -a/--artist
  -A ALBUM, --album ALBUM
                        Specify album name
  -u USERNAME, --username USERNAME
                        Specify username. Must be used with -p/--playlist
  -p PLAYLIST, --playlist PLAYLIST
                        Specify playlist name. Must be used with -u/--username
  -l LOCATION, --location LOCATION
                        Specify a directory to place files in.
  -o, --organize        Organize downloaded files.
  -c, --config          Display path to config file.
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

To download metadata through spotify, you'll want to head to their Dev Apps page, [here](https://developer.spotify.com/my-applications/). After doing that you'll want to create a new app. Name it whatever you want and then once you've done that, find the `Client ID` and `Client Secret` keys. You'll want to take those keys and paste them into your system's environment variables as `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`, correspondingly. Viola! You can now download metadata with IRS!

## Metadata

Currently, the program attaches the following metadata to the downloaded files:
 - Title
 - Artist
 - Album
 - Album Art
 - Genre
 - Track Number
 - Disc Number
 - Compilation (iTunes only)

## Philosophy

When I made this program I was pretty much broke and my music addiction wasn't really helping that problem. So, I did the obvious thing: make an uber-complicated program to ~~steal~~ download music for me! As for the name, its acronym spells IRS, which I found amusing, seeing as the IRS ~~takes~~ steals money while my program ~~gives~~ reimburses you with music.

The design/style inspiration of pretty much everything goes to [k4m4](https://github.com/k4m4).

## Wishlist

 - [x] Full album downloading
 - [x] Album art metadata correctly displayed
 - [x] Spotify playlist downloading
 - [ ] GUI/Console interactive version - *in progress*
 - [ ] Lyric metadata
 - [ ] 99% success rate for automatic song choosing
