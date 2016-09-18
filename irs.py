import mutagen.id3, mutagen.easyid3, mutagen.mp3, youtube_dl
import urllib.request, urllib.parse, re, sys, os, requests
from bs4 import BeautifulSoup

def search_google(song, artist, search_terms=""):
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True
    string = "%s %s %s" % (song, artist, search_terms)
    filename = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(string)
    hdr = {
    'User-Agent':'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    texts = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(filename, \
    headers=hdr)).read(), 'html.parser').findAll(text=True)
    return list(filter(visible, texts))

def parse_metadata(song, artist, location, filename, tracknum="", album=""):
    googled = search_google(song, artist)
    mp3file = mutagen.mp3.MP3("%s/%s" % (location, filename), ID3=mutagen.easyid3.EasyID3)
    print ("%s Metadata parsing:" % color('[+]','OKBLUE'))

    # Song title
    mp3file['title'] = song
    mp3file.save()
    print ("\t%s Title parsed: " % color('[+]','OKGREEN') + mp3file['title'][0])

    # Artist
    mp3file['artist'] = artist
    mp3file.save()
    print ("\t%s Artist parsed: " % color('[+]','OKGREEN') + mp3file['artist'][0])

    # Album
    if album == "":
        for i, j in enumerate(googled):
            if "Album:" in j:
                album = (googled[i + 1])
    try:
        mp3file['album'] = album
        print ("\t%s Album parsed: " % color('[+]','OKGREEN') + mp3file['album'][0])
    except Exception:
        mp3file['album'] = album
        print ("\t%s Album not parsed" % color('[-]','FAIL'))
    mp3file.save()

    # Album art
    if mp3file['album'][0] != "":
        try:
            download_album_art(mp3file['album'][0], artist, location=location)
            embed_mp3("%s/cover.jpg" % location, "%s/%s" % (location, filename))
            print ("\t%s Album art parsed" % color('[+]','OKGREEN'))
        except Exception as e:
            print ("\t%s Album art not parsed" % color('[-]','FAIL'))

    # Release date
    for i, j in enumerate(googled):
        if "Released:" in j:
            date = (googled[i + 1])
    try:
        mp3file['date'] = date
        print ("\t%s Release date parsed" % color('[+]','OKGREEN'))
    except Exception:
        mp3file['date'] = ""
    mp3file.save()

    # Track number
    if tracknum != "":
        mp3file['tracknumber'] = str(tracknum)
        mp3file.save()

    print ("\n%s \"%s\" downloaded successfully!\n" % (color('[+]','OKGREEN'), song))

def embed_mp3(art_location, song_location):
    music = mutagen.id3.ID3(song_location)
    music.delall("APIC")
    music.add(mutagen.id3.APIC(encoding=0, mime="image/jpg", type=3, desc='', \
    data=open(art_location, 'rb').read()))
    music.save()

def download_album_art(album, artist, location=""):
    try:
        search = "%s %s" % (album, artist)
        url = "http://www.seekacover.com/cd/" + urllib.parse.quote_plus(search)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        done = False
        for img in soup.findAll('img'):
            if done == False:
                try:
                    if search.lower() in img['title'].lower():
                        urllib.request.urlretrieve(img['src'], "%s/cover.jpg" % location)
                        done = True
                except Exception:
                    pass
    except Exception:
        pass

def strip_special_chars(string):
    special_chars = "\ / : * ? \" < > | - ( )".split(" ")
    for char in special_chars:
        string.replace(char, "")
    return string

def color(text, type):
    types = {'HEADER': '\033[95m', 'OKBLUE': '\033[94m', 'OKGREEN': '\033[92m',
    'WARNING': '\033[93m','FAIL': '\033[91m','ENDC': '\033[0m','BOLD': '\033[1m'
    ,'UNDERLINE': '\033[4m'}
    return types[type] + text + types['ENDC']

def find_mp3(song, artist):
    search_terms = song + " " + artist
    print ("\"%s\" by %s" % (song, artist))
    query_string = urllib.parse.urlencode({"search_query" : (search_terms)})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    in_title = False
    i = -1
    given_up_score = 0
    while in_title == False:
        i += 1
        given_up_score += 1
        if given_up_score >= 10:
            in_title = True
        audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
        title = strip_special_chars((BeautifulSoup(urllib.request.urlopen(audio_url), 'html.parser')).title.string.lower())
        song_title = song.lower().split("/")
        for song in song_title:
            if strip_special_chars(song) in strip_special_chars(title):
                in_title = True
    return search_results[i]

def rip_album(album, artist, tried=False, search="album"):
    visible_texts = search_google(album, artist, search)
    try:
        songs = []
        num = True
        for i, j in enumerate(visible_texts):
            if 'Songs' in j:
                if visible_texts[i + 1] == "1":
                    indexed = i
        while num == True:
            try:
                if type(int(visible_texts[indexed])) is int:
                    a = visible_texts[indexed + 1]
                    songs.append(a)
                    indexed += 1
            except:
                indexed += 1
                if indexed >= 1000:
                    num = False
                else:
                    pass

        for i, j in enumerate(songs):
            rip_mp3(j, artist, part_of_album=True, album=album, tracknum=i + 1)

    except Exception as e:
        if str(e) == "local variable 'indexed' referenced before assignment" or str(e) == 'list index out of range':
            if tried != True:
                print ("%s Trying to find album ..." % color('[*]','OKBLUE'))
                rip_album(album, artist, tried=True, search="")
            else:
                print ("%s Could not find album '%s'" % (color('[-]','FAIL'), album))
        else:
            print ("%s There was an error with getting the contents \
of the album '%s'" % (color('[-]','FAIL'), album))

def rip_mp3(song, artist, part_of_album=False, album="", tracknum=""):
    audio_code = find_mp3(song, artist)
    filename = strip_special_chars(song) + ".mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        #'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["http://www.youtube.com/watch?v=" + audio_code])

    artist_folder = artist
    if not os.path.isdir(artist_folder):
        os.makedirs(artist_folder)
    if not part_of_album:
        location = artist_folder

    if album != "" and part_of_album:
        album_folder = artist + "/" + album
        if not os.path.isdir(album_folder):
            os.makedirs(album_folder)
        location = album_folder

    for file in os.listdir("."):
        if audio_code in file:
            os.rename(file, location + "/" + filename)

    parse_metadata(song, artist, location, filename, tracknum=tracknum, album=album)

def main():
    media = sys.argv[1]
    args = " ".join(sys.argv[2:]).split(" by ")
    if media == "song":
        rip_mp3(args[0], args[1])
    elif media == "album":
        rip_album(args[0], args[1])

if __name__ == '__main__':
    main()
