import sys
import re

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
elif sys.version_info[0] < 3:
    from urllib import urlencode
    from urllib import urlopen
else:
    print("Must be using Python 2 or 3")
    sys.exit(1)

from bs4 import BeautifulSoup


def find_url(song_title, artist_name, search_terms=None, caught_by_google=False, download_first=False):
    """Finds the youtube video url for the requested song. The youtube 
        query is constructed like this:
        "<song> <artist> <search terms>"
        so plugging in "Bohemian Rhapsody", "Queen", and "lyrics" would end
        up with a search for "Bohemian Rhapsody Queen lyrics" on youtube
    :param-required song: song name
    :param-required artist: artist name
    :param search_terms: any additional search terms you may want to
        add to the search query
    :param caught_by_google: a boolean, if not false or none, turns on
        the captcha catcher
    :param download_first: a boolean, if true, downloads first video
        that youtube returns
    :rtype: A string of the youtube url for the song
    """

    query = artist_name + " " + song_title
    if search_terms:
        query += " " + search_terms

    encoded_query = urlencode({"search_query": query})

    url = "http://www.youtube.com/results?" + encoded_query

    soup = _get_url_data(url, caught_by_google)

    # if you want to inspect the html being requested
    # print(soup.prettify())
    # with open("index.html", "wb") as f:
    #     f.write(soup.prettify().encode('utf-8'))

    # Each of the tags in the results list have the following relevant 
    # attributes:
    #   "title": the title of the youtube video
    #   "href": the youtube video code, namely the X's of 
    #       https://www.youtube.com/watch?v=XXXXXXXXXXX
    #   "class": the classes of the link, used to identify the youtube title
    results = _find_links(soup)

    best_guess = None
    total_tries_counter = 0

    if len(results) <= 0:
        raise Exception('There were no search results for "{}"'.format(query))

    if download_first == True:
        return "https://youtube.com" + results[0]["href"]

    scores = []

    for index, link in enumerate(results):
        scores.append([
            index, 
            _score_song(song_title, artist_name, link["title"]),
            link["href"]
        ])

    # sort by the score of the song
    sorted(scores, key=lambda x: x[1])

    return "https://youtube.com" + results[scores[0][0]]["href"]


def _score_song(song_title, artist_name, video_title):
    """Scores the likelihood of the song audio being in the video based off of
        the video title.
    :param song_title: a string, the title of the song that you're looking for
    :param video_title: a string, the title of the video you're analyzing
    :rtype: an integer, the score of the song
    """
    points = 0

    song_title = _simplify(song_title)
    artist_name = _simplify(artist_name)
    video_title = _simplify(video_title)

    if song_title in video_title:
        points += 3

    if artist_name in video_title:
        points += 3

    points -= _count_garbage_phrases(video_title, song_title)

    return points
    

def _simplify(string):
    """Lowercases and strips all non alphanumeric characters from the string
    :param string: a string to be modified
    :rtype: the modified string
    """
    if type(string) == bytes:
        string = string.decode()
    return re.sub(r'[^a-zA-Z0-9]+', '', string.lower())


def _count_garbage_phrases(video_title, song_title):
    """Checks if there are any phrases in the title of the video that would 
        indicate it doesn't have the audio we want
    :param string: a string, the youtube video title
    :param title: a string, the actual title of the song we're looking for
    :rtype: an integer, of the number of bad phrases in the song
    """

    # Garbage phrases found through experiences of downloading the wrong song
    # TODO: add this into the config so the user can mess with it if they want
    garbage_phrases = (
        "cover  album  live  clean  rare version  full  full album  row  at  "
        "@  session  how to  npr music  reimagined  hr version"
    ).split("  ")

    bad_phrases = 0

    for gphrase in garbage_phrases:
        # make sure we're not invalidating part of the title of the song
        if gphrase in song_title.lower():
            continue
        
        # check if the garbage phrase is not in the video title
        if gphrase in video_title.lower():
            bad_phrases += 1
    
    return bad_phrases


def _find_links(soup):
    """Finds youtube video links in the html soup
    :param soup: a BeautifulSoup(...) element
    :rtype: returns a list of valid youtube video links
    """
    return list(filter(None, map(_find_link, soup.find_all("a"))))


def _find_link(link):
    """Tests html tags to see if they contain a youtube video link.
        Should be used only with the find_links function in a map func.
    :param link: accepts an element from BeautifulSoup(...).find_all(...)
    :rtype: returns the link if it's an actual video link, otherwise, None
    """
    try:
        class_to_check = str(" ".join(link["class"]))
    except KeyError:
        return

    # these classes are found by inspecting the html soup of a youtube search.
    valid_classes = [
        "yt-simple-endpoint style-scope ytd-video-renderer",
        ("yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 "
         "yt-uix-sessionlink spf-link ")
    ]

    try:
        # Make sure it's not a playlist
        if "&list=" in link["href"]:
            return

        for valid_class in valid_classes:
            if valid_class in class_to_check:
                return link
    except KeyError:
        pass


# TODO: build in the captcha cheater if the user is "caught" by google
def _get_url_data(url, caught_by_google):
    """Gets parsed html from the specified url
    :param url: A string, the url to request and parse.
    :param caught_by_google: A boolean, will open and use the captcha 
        cheat to get around google's captcha.
    :rtype: A BeautifulSoup class
    """
    html_content = urlopen(url).read()
    return BeautifulSoup(html_content, 'html.parser')