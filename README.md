# The Ingenious Redistribution System (IRS)

Downloads or streams media from the name of the song / album / movie / tv-show that you requested.

### Dependencies

First, actually install python and pip:
 - To install python3 and `pip` for Ubuntu run this command:

 ```bash
 $ sudo apt-get install python3 python3-pip
 ```
 - For Windows follow [this](http://www.howtogeek.com/197947/how-to-install-python-on-windows/) guide to install python (remember to install ~v3.4), and [this](https://pip.pypa.io/en/latest/installing/) guide to install `pip`.
 - For OSX follow [this](http://docs.python-guide.org/en/latest/starting/install/osx/) guide that goes through python and `pip`. Also, remember to install ~v3.4.

Then install `requirements.txt` from the repository:
```bash
$ pip install -r requirements.txt
```

There are some more external command-line programs that are essential to movies, tv-shows, and streaming:
 - rTorrent: [Windows](https://rtwi.jmk.hu/wiki/rTorrentOnWindows), [OSX](http://macappstore.org/rtorrent/), Ubuntu:

 ```bash
 $ sudo apt-get install rtorrent
 ```
 - mpv: https://mpv.io/installation/
 - Peerflix:
   - Windows: follow [this](http://blog.teamtreehouse.com/install-node-js-npm-windows) guide to install npm and then run this command:
   ```bash
   $ npm install -g peerflix
   ```
   - OSX: Same as Windows, except follow [this](http://blog.teamtreehouse.com/install-node-js-npm-mac) guide.
   - Ubuntu: Again, the same, only follow [this](http://blog.teamtreehouse.com/install-node-js-npm-linux) guide instead.

### Install

```bash
$ git clone https://github.com/kepoorhampond/IngeniousRedistributionSystem.git
```
And that should be it! Eventually it'll be put up on `pip`, to make it much, much easier to install.

### Overview

Currently the system can stream or download the following:
 - Specific songs.
 - Complete albums.
 - Movies.
 - TV shows.
 - Playlists.
 - Links
 - Comics and books.*

<sup>\* Limited only to downloading.<sup>

When downloading music, the system will fill out the specific meta-data so that it will appear organized in your player of choice. It parses the following pieces of meta-data:
 - Title.
 - Artist.
 - Album.
 - Album cover/art.*
 - Year released.
 - Tracknumber.*

<sup>\* Album art is slightly buggy, and tracknumber only works when downloading complete album.<sup>

On a personal judgement, we would say that the complete meta-data parsing works ~80% of the time.

### Usage
```bash
$ irs (stream | download) movie <movie-name>
$ irs (stream | download) tv <tv-show> <episode>
$ irs (stream | download) (song | album) <title> by <artist>
$ irs (stream | download) playlist <txt-file-name>
irs (stream | download) '<link>' <title> <author>
$ irs download (comic <title> <run> | book <title> by <author>)
```

#### Examples
```bash
$ irs download book I, Robot by Isaac Asimov
$ irs stream song Where Is My Mind by The Pixies
$ irs download album A Night At The Opera by Queen
$ irs stream movie Fight Club
$ irs download tv mr.robot s01e01
$ irs stream playlist "Rock Save The Queen.txt"
$ irs download comic Paper Girls 001
$ irs download link 'https://www.youtube.com/watch?v=5sy2qLtrQQQ' "Stranger Things OST" "Kyle Dixon and Michael Stein"
```

The text file should be formatted like so: `<song>: <artist>`
```
Good Times Bad Times: Led Zeppelin
I Want To Break Free: Queen
The Man Who Sold The World: David Bowie
```

### Disclaimer
Copyrighted content may be illegal to stream and/or download in your country.
