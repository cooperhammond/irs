class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[30m'
    YELLOW = '\033[33m'

def choose_from_spotify_list(thelist):
    thelist = list(thelist)
    print ("Results:")
    choice = ""
    while choice not in tuple(range(0, len(thelist[:5]))):
        for index, result in enumerate(thelist[:5]):
            type = result["type"]

            if type == "playlist":
                info = spotify.user(result["owner"]["id"])
                try:
                    display_info = " (" + str(info["followers"]["total"]) + " followers)"
                    display_info += " - " + info["display_name"]
                except Exception:
                    display_info = " - info couldn't be found"

            elif type == "album":
                info = spotify.album(result["id"])
                display_info = " - " + info["artists"][0]["name"]

            print ("\t" + str(index) + ") " + result["name"] + display_info)
        choice = int(input(bc.YELLOW + "\nEnter result number: " + bc.ENDC))

    return thelist[choice]

def rip_spotify_list(search, type, id=None):
    spotify = spotipy.Spotify()

    results = spotify.search(q=search, type=type)
    items = results[type + "s"]['items']
    songs = []
    if len(items) > 0:
        spotify_list = choose_from_spotify_list(items)
        list_type = spotify_list["type"]
        if list_type != "playlist":
            spotify_list = eval("spotify.%s" % list_type)(spotify_list["uri"])
        else:
            try:
                spotify_list = spotify.user_playlist(spotify_list["owner"]["id"], \
                playlist_id=spotify_list["uri"], fields="tracks,next")
            except spotipy.client.SpotifyException:
                print (bc.FAIL + "To download Spotify playlists, you need to supply client_id's" + bc.ENDC)
                exit(1)

        print (bc.YELLOW + "\nFetching tracks ..." + bc.ENDC, end="\r")
        for song in spotify_list["tracks"]["items"]:
            artist = spotify.artist(song["artists"][0]["id"])
            songs.append([song["name"], artist["name"]])
        print (bc.OKGREEN + "Found tracks!" + bc.ENDC)
        return songs
    else:
        print (bc.FAIL + "No results were found." + bc.ENDC)
        exit(1)

import spotipy

spotify = spotipy.Spotify()

#results = spotify.search(q="Star Wars Headspace", type="album")

#results = results["albums"]["items"]


print (rip_spotify_list("Brain Food", "playlist"))
