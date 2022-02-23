# irs: The Ironic Repositioning System

[![made-with-crystal](https://img.shields.io/badge/Made%20with-Crystal-1f425f.svg?style=flat-square)](https://crystal-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/cooperhammond/irs/blob/master/LICENSE)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg?style=flat-square)](https://saythanks.io/to/kepoorh%40gmail.com)

> A music scraper that understands your metadata needs.

`irs` is a command-line application that downloads audio and metadata in order
to package an mp3 with both. Extensible, the user can download individual 
songs, entire albums, or playlists from Spotify.

<p align="center">
    <img src="https://i.imgur.com/7QTM6rD.png" height="400" title="#1F816D" />
</p>
<p align="center"

[![forthebadge](https://forthebadge.com/images/badges/compatibility-betamax.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/ages-18.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-by-codebabes.svg)](https://forthebadge.com)
</p>

---

## Table of Contents

- [Usage](#usage)
    - [Demo](#demo)
- [Installation](#installation)
    - [Pre-built](#pre-built)
    - [From source](#from-source)
    - [Set up](#setup)
- [Config](#config)
- [How it works](#how-it-works)
- [Contributing](#contributing)


## Usage

```
~ $ irs -h

Usage: irs [--help] [--version] [--install]
           [-s <song> -a <artist>]
           [-A <album> -a <artist>]
           [-p <playlist> -a <username>]

Arguments:
    -h, --help                  Show this help message and exit
    -v, --version               Show the program version and exit
    -i, --install               Download binaries to config location
    -c, --config                Show config file location
    -a, --artist <artist>       Specify artist name for downloading
    -s, --song <song>           Specify song name to download
    -A, --album <album>         Specify the album name to download
    -p, --playlist <playlist>   Specify the playlist name to download
    -u, --url <url>             Specify the youtube url to download from (for single songs only)
    -g, --give-url              Specify the youtube url sources while downloading (for albums or playlists only only)

Examples:
    $ irs --song "Bohemian Rhapsody" --artist "Queen"
    # => downloads the song "Bohemian Rhapsody" by "Queen"
    $ irs --album "Demon Days" --artist "Gorillaz"
    # => downloads the album "Demon Days" by "Gorillaz"
    $ irs --playlist "a different drummer" --artist "prakkillian"
    # => downloads the playlist "a different drummer" by the user prakkillian
```

### Demo

[![asciicast](https://asciinema.org/a/332793.svg)](https://asciinema.org/a/332793)

## Installation

### Pre-built 

Just download the latest release for your platform 
[here](https://github.com/cooperhammond/irs/releases).

Note that the binaries right now have only been tested on WSL. They *should* run on most linux distros, and OS X, but if they don't please make an issue above.

### From Source

If you're one of those cool people who compiles from source

1. Install crystal-lang 
    ([`https://crystal-lang.org/install/`](https://crystal-lang.org/install/))
1. Clone it (`git clone https://github.com/cooperhammond/irs`)
1. CD it (`cd irs`)
1. Build it (`shards build`)

### Setup

1. Create a `.yaml` config file somewhere on your system (usually `~/.irs/`)
1. Copy the following into it
    ```yaml
    binary_directory: ~/.irs/bin
    music_directory: ~/Music
    filename_pattern: "{track_number} - {title}"
    directory_pattern: "{artist}/{album}"
    client_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    client_secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    single_folder_playlist:
        enabled: true
        retain_playlist_order: true
        unify_into_album: false
    ```
1. Set the environment variable `IRS_CONFIG_LOCATION` pointing to that file
1. Go to [`https://developer.spotify.com/dashboard/`](https://developer.spotify.com/dashboard/)
1. Log in or create an account
1. Click `CREATE A CLIENT ID`
1. Enter all necessary info, true or false, continue
1. Find your client key and client secret
1. Copy each respectively into the X's in your config file
1. Run `irs --install` and answer the prompts!

You should be good to go! Run the file from your command line to get more help on
usage or keep reading!

# Config

You may have noticed that there's a config file with more than a few options. 
Here's what they do:
```yaml
binary_directory: ~/.irs/bin
music_directory: ~/Music
search_terms: "lyrics"
filename_pattern: "{track_number} - {title}"
directory_pattern: "{artist}/{album}"
client_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
client_secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
single_folder_playlist:
    enabled: true
    retain_playlist_order: true
    unify_into_album: false
```
 - `binary_directory`: a path specifying where the downloaded binaries should
    be placed
 - `music_directory`: a path specifying where downloaded mp3s should be placed.
 - `search_terms`: additional search terms to plug into youtube, which can be
    potentially useful for not grabbing erroneous audio.
 - `filename_pattern`: a pattern for the output filename of the mp3
 - `directory_pattern`: a pattern for the folder structure your mp3s are saved in
 - `client_key`: a client key from your spotify API application
 - `client_secret`: a client secret key from your spotify API application
 - `single_folder_playlist/enabled`: if set to true, all mp3s from a downloaded
    playlist will be placed in the same folder.
 - `single_folder_playlist/retain_playlist_order`: if set to true, the track 
    numbers of the mp3s of the playlist will be overwritten to correspond to
    their place in the playlist
 - `single_folder_playlist/unify_into_album`: if set to true, will overwrite
    the album name and album image of the mp3 with the title of your playlist
    and the image for your playlist respectively


In a pattern following keywords will be replaced:

| Keyword | Replacement | Example |
| :----: | :----: | :----: |
| `{artist}` | Artist Name | Queen |
| `{title}` | Track Title | Bohemian Rhapsody |
| `{album}` | Album Name | Stone Cold Classics |
| `{track_number}` | Track Number | 9 |
| `{total_tracks}` | Total Tracks in Album | 14 |
| `{disc_number}` | Disc Number | 1 |
| `{day}` | Release Day | 01 |
| `{month}` | Release Month | 01 |
| `{year}` | Release Year | 2006 |
| `{id}` | Spotify ID | 6l8GvAyoUZwWDgF1e4822w |

Beware OS-restrictions when naming your mp3s.

Pattern Examples:
```yaml
music_directory: ~/Music
filename_pattern: "{track_number} - {title}"
directory_pattern: "{artist}/{album}"
```
Outputs: `~/Music/Queen/Stone Cold Classics/9 - Bohemian Rhapsody.mp3`
<br><br>
```yaml
music_directory: ~/Music
filename_pattern: "{artist} - {title}"
directory_pattern: ""
```
Outputs: `~/Music/Queen - Bohemian Rhapsody.mp3`
<br><br>
```yaml
music_directory: ~/Music
filename_pattern: "{track_number} of {total_tracks} - {title}"
directory_pattern: "{year}/{artist}/{album}"
```
Outputs: `~/Music/2006/Queen/Stone Cold Classics/9 of 14 - Bohemian Rhapsody.mp3`
<br><br>
```yaml
music_directory: ~/Music
filename_pattern: "{track_number}. {title}"
directory_pattern: "irs/{artist} - {album}"
```
Outputs: `~/Music/irs/Queen - Stone Cold Classics/9. Bohemian Rhapsody.mp3`
<br>


## How it works

**At it's core** `irs` downloads individual songs. It does this by interfacing
with the Spotify API, grabbing metadata, and then searching Youtube for a video
containing the song's audio. It will download the video using 
[`youtube-dl`](https://github.com/ytdl-org/youtube-dl), extract the audio using
[`ffmpeg`](https://ffmpeg.org/), and then pack the audio and metadata together
into an MP3.

From the core, it has been extended to download the index of albums and 
playlists through the spotify API, and then iteratively use the method above
for downloading each song.

It used to be in python, but
1. I wasn't a fan of python's limited ability to distribute standalone binaries
1. It was a charlie foxtrot of code that I made when I was little and I wanted
    to refine it
1. `crystal-lang` made some promises and I was interested in seeing how well it
    did (verdict: if you're building high-level tools you want to run quickly 
    and distribute, it's perfect)


## Contributing

Any and all contributions are welcome. If you think of a cool feature, send a 
PR or shoot me an [email](mailto:kepoorh@gmail.com). If you think something 
could be implemented better, _please_ shoot me an email. If you like what I'm
doing here, _pretty please_ shoot me an email.

1. Fork it (<https://github.com/your-github-user/irs/fork>)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
