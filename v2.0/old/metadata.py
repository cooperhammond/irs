

def parse_metadata(song, artist, location, filename,
    tracknum="",
    album="",
    album_art_url=""
        ):
        
    # Release date
    for i, j in enumerate(googled):
        if "Released:" in j:
            date = (googled[i + 1])

    try:
        mp3file['date'] = date
        print (bc.OKGREEN + "Release date parsed: " + bc.ENDC + mp3file['date'][0])
    except Exception:
        mp3file['date'] = ""
        pass

    mp3file.save()


    # Track number
    if tracknum:
        mp3file['tracknumber'] = str(tracknum)
        mp3file.save()


    # Album art
    try:
        if album:
            if not album_art_url:
                print (bc.YELLOW + "Parsing album art ..." + bc.ENDC, end="\r")
                temp_url = get_albumart_url(album, artist)
                embed_mp3(temp_url, location + "/" + filename)
                print (bc.OKGREEN + "Album art parsed: " + bc.ENDC + temp_url)

            else: # If part of an album, it should do this.
                embed_mp3(album_art_url, location + "/" + filename)
                print (bc.OKGREEN + "Album art parsed." + bc.ENDC)


    except Exception as e:
        print (bc.FAIL + "Album art not parsed: " + bc.ENDC + str(e))

def embed_mp3(albumart_url, song_location):
    image = urlopen(albumart_url)
    audio = EasyMP3(song_location, ID3=ID3)

    try:
        audio.add_tags()
    except Exception as e:
        pass

    audio.tags.add(
        APIC(
            encoding = 3,
            mime = 'image/png',
            type = 3,
            desc = 'Cover',
            data = image.read()
        )
    )
    audio.save()

def get_albumart_url(album, artist):
    def test_404(url):
        try:
            urlopen(albumart).read()
        except Exception:
            return False
        return True

    tries = 0
    album = "%s %s Album Art" % (artist, album)
    url = ("https://www.google.com/search?q=" + quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
    header = {
        'User-Agent':
            '''
                Mozilla/5.0 (Windows NT 6.1; WOW64)
                AppleWebKit/537.36 (KHTML,like Gecko)
                Chrome/43.0.2357.134 Safari/537.36
            '''
    }

    soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

    albumart_divs = soup.findAll("div", {"class": "rg_meta"})
    albumart = json.loads(albumart_divs[tries].text)["ou"]

    while not test_404(albumart):
        tries += 1
        albumart = json.loads(albumart_divs[tries].text)["ou"]

    return albumart
