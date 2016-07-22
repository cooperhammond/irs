#!/usr/bin/python3
#    Ingenious Redistribution System, A system built to redistribute media to the consumer.
#    Copyright (C) 2016  Cooper Hammond
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, time, re, select, requests, subprocess
import urllib.request, urllib.parse
from termcolor import colored
from urllib.request import Request, urlopen

from mutagen.id3 import APIC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
import youtube_dl, mutagen

def download_album_art(album, band):
    search = "%s %s" % (album, band)
    url = "http://www.seekacover.com/cd/" + urllib.parse.quote_plus(search)
    page = requests.get(url).text
    soup = BeautifulSoup(page)
    done = False
    for img in soup.findAll('img'):
        if done == False:
            try:
                if search.lower() in img['title'].lower():
                    url = img['src']
                    urllib.request.urlretrieve(url, "cover.jpg")
                    done = True
            except Exception:
                pass

def embed_mp3(art_location, song_path):
    music = mutagen.id3.ID3(song_path)

    music.delall('APIC')

    music.add(APIC(
        encoding=0,
        mime="image/jpg",
        type=3,
        desc='',
        data=open(art_location, "rb").read()
        )
    )
    music.save()

def find_mp3(song, author): #
    print ("\n'%s' by '%s'" % (song, author))
    query_string = urllib.parse.urlencode({"search_query" : ("%s %s lyrics" % (song, author))})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    in_song = False
    i = -1
    given_up_score = 0
    while in_song == False:
        if given_up_score >= 10:
            in_song = True
        i += 1
        audio_url = ("http://www.youtube.com/watch?v=" + search_results[i])
        title = (BeautifulSoup(urlopen(audio_url), 'html.parser')).title.string.lower()
        if song.lower() in title:
            in_song = True
        else:
            given_up_score += 1
    return audio_url

def rip_mp3(song, author, album, tracknum):
    audio_url = find_mp3(song, author)
    command = 'youtube-dl --metadata-from-title "%(title)s" --extract-audio --audio-format mp3 --add-metadata ' + audio_url
    os.system(command)
    for filename in os.listdir("."):
        if str(audio_url).strip("http://www.youtube.com/watch?v=") in filename:
            os.rename(filename, song + ".mp3")

    try:
        googled = search_google(song, author)
        mp3file = MP3(song + ".mp3", ID3=EasyID3)
        print ("\n%s Metadata parsing:" % output("s"))
        try:
            mp3file['title'] = song
        except Exception:
            mp3file['title'] = ""
        mp3file.save()
        print ('\t%s Title parsed: %s' % (output("g"), mp3file['title']))

        mp3file['artist'] = author
        mp3file.save()
        print ('\t%s Author parsed: %s' % (output("g"), mp3file['artist']))
        if album == "":
            for i, j in enumerate(googled):
                if "Album:" in j:
                    album = (googled[i + 1])
            try:
                mp3file['album'] = album
                mp3file.save()
            except Exception:
                mp3file['album'] = ""
                mp3file.save()
            print ('\t%s Album Auto-parsed: %s' % (output("g"), mp3file['album']))
        else:
            try:
                mp3file['album'] = album
                mp3file.save()
            except Exception:
                mp3file['album'] = ""
                mp3file.save()
            print ('\t%s Album parsed: %s' % (output("g"), mp3file['album']))

        if mp3file['album'][0] != "":
            try:
                download_album_art(mp3file['album'][0], author)
                embed_mp3("cover.jpg", song + ".mp3")
                print ("\t%s Album art Auto-parsed!" % output("g"))
            except Exception as e:
                print ("%s There was a problem with Auto-parsing the album art of: '%s'" % (output("e"), song))
                print (e)

        for i, j in enumerate(googled):
            if "Released:" in j:
                date = (googled[i + 1])
        try:
            mp3file['date'] = date
        except Exception:
            mp3file['date'] = ""
        mp3file.save()
        print ('\t%s Release date Auto-parsed: "%s"' % (output("g"), mp3file['date'][0]))

        if tracknum != "":
            mp3file['tracknumber'] = str(tracknum)
            mp3file.save()

        print ('\n%s "' % output("g") + song + '" by ' + author + ' downloaded successfully\n')
    except Exception as e:
        print (e)

def output(string):
    if string == "q":
        return colored("[?]", "cyan", attrs=['bold'])
    elif string == "e":
        return colored("[-]", "red", attrs=['bold'])
    elif string == "g":
        return colored("[+]", "green", attrs=['bold'])
    elif string == "s":
        return colored("[*]", "blue", attrs=['bold'])

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def search_google(song_name, band):
    try:
        string = "%s %s" % (song_name, band)
        filename = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(string)
        hdr = {
        'User-Agent':'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        texts = BeautifulSoup(urlopen(Request(filename, headers=hdr)).read(), 'html.parser').findAll(text=True)

        visible_texts = list(filter(visible, texts))
        return visible_texts
    except Exception as e:
        print ("%s There was an error with Auto-parsing." % output("e"))
        return ""

def get_album(album_name, artist, what_to_do):
    visible_texts = search_google(album_name, artist)
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
    if what_to_do == "download":
        for i, j in enumerate(songs):
            rip_mp3(j, artist, album_name, i + 1)
    elif what_to_do == "stream":
        for i in songs:
            a = find_mp3(i, artist)
            command = 'mpv "%s" --no-video' % a
            os.system(command)


def get_torrent_url(args, category):
    search_url = 'https://kat.cr/usearch/' + urllib.parse.quote_plus((" ".join(args) + " category:" + category))
    search_request_response = requests.get(search_url, verify=True)
    soup = BeautifulSoup(search_request_response.text, 'html.parser')
    results, ran_out = 0, False
    i = 0
    print ("")
    while True:
        movie_page = soup.find_all("a", class_="cellMainLink")
        for number in range(0,10):
            try:
                print ("%s. " % (number + 1) + movie_page[number].string)
                results += 1
            except Exception:
                ran_out = True
                pass
        if ran_out == True:
            if results == 0:
                print (output('e') + " No results.\n")
                exit(0)
            else:
                print (output('e') + " End of results.")
        if results != 0:

            try: a = int(str(input("\n%s What torrent would you like? " % output("q")))) - 1
            except Exception: a = 100; pass
            # This code is either hyper-efficient, or completely against every ettiquite.

            if a in tuple(range(0, 10)):
                search_url = requests.get('https://kat.cr' + movie_page[a].get('href'), verify=True)
                soup = BeautifulSoup(search_url.text, 'html.parser')
                torrent_url = 'https:' + soup.find_all('a', class_='siteButton')[0].get('href')
                return torrent_url

def rip_playlist(file_name, what_to_do):
    txt_file = open(file_name, 'r')
    things_that_went_wrong = []
    something_went_wrong = False
    for line in txt_file:
        try:
            arr = line.split(": ")
            song = arr[0]
            artist = arr[1]
            if what_to_do == "download":
                rip_mp3(song, artist, "", "")
            elif what_to_do == "stream":
                os.system("mpv '%s' --no-video" % find_mp3(song, artist))
        except Exception as e:
            something_went_wrong = True
            things_that_went_wrong.append(line)
            pass
    if something_went_wrong == True:
        print ("%s Something was wrong with the formatting of the following lines:" % output("e"))
        for i in things_that_went_wrong: print ("\t%s" % i)

def main():
    try:
        i = 0
        args = sys.argv
        del args[i]
        what_to_do = args[i]
        del args[i]

        if what_to_do not in ("download", "stream"): raise Exception("no what-to-do")

        media = args[i]
        del args[i]

        if media == "song":
            song = (" ".join(args)).split(" by ")
            if what_to_do == "stream":
                command = 'mpv "%s" --no-video' % find_mp3(song[0], song[1])
                os.system(command)
            elif what_to_do == "download":
                rip_mp3(song[0], song[1], "", "")

        elif media == "album":
            album_name = (" ".join(args)).split(" by ")
            get_album(album_name[0], album_name[1], what_to_do)

        elif media == "playlist":
            rip_playlist(args[-1], what_to_do)

        elif media in ("comic", "book"):
            if what_to_do == "download":
                os.system("rtorrent '%s'" % get_torrent_url(args, media + "s"))
                exit(0)
            elif what_to_do == "stream":
                print ("\n%s Streaming is unavailable for comics and books.\n" % output("e"))
                exit(0)

        elif media == "movie":
            if what_to_do == "stream":
                os.system('peerflix "%s" -a -d --mpv' % get_torrent_url(args, 'movie'))
                exit(0)
            elif what_to_do == "download":
                os.system("rtorrent '%s'" % get_torrent_url(args, 'movie'))
                exit(0)

        elif media == "tv":
            if what_to_do == "stream":
                os.system('peerflix "%s" -a -d --mpv' % get_torrent_url(args, 'tv'))
                exit(0)
            elif what_to_do == "download":
                os.system("rtorrent '%s'" % get_torrent_url(args, 'tv'))
                exit(0)
        else:
            raise Exception("no media")
    except Exception as e:
        if str(e) in ("list index out of range", "no what-to-do", "no media"):
            print ("%s Either you used an invalid format, or a special character.\n" % output("e"))
            invalid_format()
        else:
            print ("%s Something went wrong:\n" % output("e") + repr(e) + "\n")

def invalid_format():
    # I feel like there should be an easier way to write out help for command-line interfaces ...
    print ("Usage:")
    print ("""    irs (stream | download) movie <movie-name>
    irs (stream | download) tv <tv-show> <episode>
    irs (stream | download) (song | album) <title> by <artist>
    irs (stream | download) playlist <txt-file-name>
    irs download (comic <title> <run> | book <title> by <author>) """)
    print ("Examples:")
    print ("""    irs download book I, Robot by Isaac Asimov
    irs stream song Where Is My Mind by The Pixies
    irs download album A Night At The Opera by Queen
    irs stream movie Fight Club
    irs download tv mr.robot s01e01
    irs stream playlist "Rock Save The Queen.txt"
    irs download comic Paper Girls 001 """)
    print ("\nFor more info see: https://github.com/kepoorhampond/IngeniousRedistributionSystem")

if __name__ == '__main__':
    main()
