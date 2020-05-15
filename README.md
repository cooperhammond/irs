# `irs`
###### AKA `Ironic Repositioning System`

[![made-with-crystal](https://img.shields.io/badge/Made%20with-Crystal-1f425f.svg?style=flat-square)](https://crystal-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/cooperhammond/irs/blob/master/LICENSE)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg?style=flat-square)](https://saythanks.io/to/kepoorhampond)

> A music scraper that understands your metadata needs.

## Installation

1. Download the latest release for your platform [here](https://github.com/cooperhammond/irs/releases)
1. Create a `.yaml` config file somewhere on your system
1. Copy the following into it
    ```yaml
    binary_directory: ~/.irs/bin
    music_directory: ~/Music
    client_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    client_secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    single_folder_playlist:
        enabled: true
        retain_playlist_order: true
        overwrite_album: false
    ```
1. Set the environment variable `IRS_CONFIG_LOCATION` pointing to that file
1. Go to [`https://developer.spotify.com/dashboard/`](https://developer.spotify.com/dashboard/)
1. Log in or create an account
1. Click `CREATE A CLIENT ID`
1. Enter all necessary info, true or false, continue
1. Find your client key and client secret
2. Copy them into where all the X's are in your config file from above

You should be good to go! Run the file from your command line to get help on usage or keep reading!

##### Optionally From Source

Or if you're one of those cool people who compiles from source

1. Install crystal-lang ([`https://crystal-lang.org/install/`](https://crystal-lang.org/install/))
1. Clone it (`git clone https://github.com/cooperhammond/irs`)
1. CD it (`cd irs`)
1. Build it (`shards build`)

## Usage

<p align="center">
    <img src="https://i.imgur.com/uYKh101.png" height="600" />
</p>

## How it works

**At it's core** `irs` downloads individual songs. It does this by interfacing with the Spotify API, grabbing metadata, and then searching Youtube for a video containing the song's audio. It will download the video using [`youtube-dl`](https://github.com/ytdl-org/youtube-dl), extract the audio using [`ffmpeg`](https://ffmpeg.org/), and then pack the audio and metadata together into an MP3.

From the core, it has been extended to download the index of albums and playlists through the spotify API, and then iteratively use the method above for downloading each song.

It used to be in `python`, but
1. I wasn't a fan of python's limited ability to distribute standalone binaries
1. It was a clusterfuck of code that I made when I was little and I wanted to refine it
2. `crystal-lang` made some promises and I was interested in seeing how well it did (verdict: if you're building high-level tools you want to run quickly and distribute, it's a joy to work in)


## Contributing

Any and all contributions are welcome. If you think of a cool feature, send a PR or shoot me an [email](mailto:kepoorh@gmail.com). If you think something could be implemented better, _please_ shoot me an email. If you like what I'm doing here, _pretty please_ shoot me an email.

1. Fork it (<https://github.com/your-github-user/irs/fork>)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request