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
python install -r requirements.txt
```

There are some more external command-line programs that are essential to movies, tv-shows, and streaming:
 - rTorrent: [Windows](https://rtwi.jmk.hu/wiki/rTorrentOnWindows), [OSX](http://macappstore.org/rtorrent/), Ubuntu: `sudo apt-get install rtorrent`
 - mpv: https://mpv.io/installation/
 - Peerflix:
   - Windows: follow [this](http://blog.teamtreehouse.com/install-node-js-npm-windows) guide to install npm and then run this command:
   ```bash
   $ npm install -g peerflix
   ```
   - OSX: Same as Windows, except follow [this](http://blog.teamtreehouse.com/install-node-js-npm-mac) guide.
   - Ubuntu: Again, the same, only follow [this](http://blog.teamtreehouse.com/install-node-js-npm-linux) guide instead.

And that should be it! Eventually it'll be put up on pip, to make it much easier to install.

### Overview

Currently the system can stream or download the following:
 - Specific songs.
 - Complete albums.
 - Movies.
 - TV shows.

When downloading music, the system will fill out the specific meta-data so that it will appear organized in your player of choice. It parses the following pieces of meta-data:
 - Title.
 - Artist.
 - Album.
 - Album cover/art.*
 - Year released.
 - Tracknumber.*

<sup>\* Album art is slightly buggy, and tracknumber only works when downloading complete album.<sup>

### Usage
```bash
$ IRS (stream | download) movie <movie-name>
$ IRS (stream | download) tv <tv-show> <episode>
$ IRS (stream | download) song <song-name> by <artist>
$ IRS (stream | download) album <album-name> by <artist>
```

##### Examples
```bash
$ IRS stream movie Fight Club
$ IRS download album A Night At The Opera by Queen
$ IRS stream song Where Is My Mind by The Pixies
$ IRS download tv mr.robot s01e01
$ IRS stream album A Day At The Races by Queen
```
### Disclaimer
Copyrighted content may be illegal to stream and/or download in your country.
