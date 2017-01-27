import sys, os, spotipy, irs

def get_config_file_path():
    return os.path.dirname(irs.__file__) + "/config.py"

def strip_special_chars(string):
    special_chars = "\ / : * ? \" < > | - ( )".split(" ")
    for char in special_chars:
        string = string.replace(char, "")
    return string

def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

if supports_color():
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
else:
    class bc:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''
        GRAY = ''
        YELLOW = ''

def color(text, colors=[]):
    if colors == []:
        raise "Must have definitions when calling color(text, colors=[])"
    color_string = ""
    for color in colors:
        color_string += "bc.%s + " % color
    color_string = color_string[:-2]
    return (bc.ENDC + eval(color_string) + text + bc.ENDC)

def color_input(text):
    print (bc.HEADER + text, end=" ")
    return input(bc.BOLD + bc.YELLOW + ": " + bc.ENDC)

def exclaim_good(text, item):
    print (bc.OKGREEN + text + bc.ENDC + item)

def test_goodness(test, word, metadata_id, mp3):
    if test:
        exclaim_good(word + " added: ", mp3.get_attr(metadata_id))
    else:
        print (bc.FAIL + word + " not added." + bc.ENDC)

def search_google(self, search_terms=""):
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif match('<!--.*-->', str(element)):
            return False
        return True

    search_terms = "%s %s %s" % (self.song, self.artist, search_terms)
    url = 'http://www.google.com/search?q=' + quote_plus(search_terms)

    hdr = {
        'User-Agent':'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    texts = BeautifulSoup(urlopen(Request(url, \
        headers=hdr)).read(), 'html.parser').findAll(text=True)

    return list(filter(visible, texts))

def unorganize(file_name, location, song_number, artist):

    locations = location.split("/")

    folder_name = ("playlist - " + file_name)[:40]

    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    os.rename(location, "%s/%s - %s" % (folder_name, song_number, locations[-1]))

    if remove:
        import shutil # Only import this if I have to.
        shutil.rmtree(locations[0])


def finish_unorganize(file_name):
    folder_name = ("playlist - " + file_name)[:40]

    os.rename(file_name, folder_name + "/" + file_name)

    os.rename(folder_name, folder_name.replace("playlist - ", ""))

def fail_oauth():
    print (bc.FAIL + "To download Spotify playlists, you need to supply client_ids." + bc.ENDC)
    print ("To do this, you'll want to create an application here:")
    print ("https://developer.spotify.com/my-applications/#!/applications/create")
    print ("Once you've done that, you'll want to copy your 'client id' and your 'client secret'")
    print ("into the config file and their corresponding locations:")
    print (get_config_file_path())
    exit(1)

def choose_from_spotify_list(thelist, length=100000):
    spotify = spotipy.Spotify()

    thelist = list(thelist)
    print ("Results:")
    choice = ""
    while choice not in tuple(range(0, len(thelist[:length]))):
        for index, result in enumerate(thelist[:length]):
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

            print ("\t" + str(index) + ") " + bc.HEADER + result["name"] + display_info + bc.ENDC)
        choice = int(input(bc.YELLOW + "\nEnter result number: " + bc.ENDC))

    return thelist[choice]

def drawProgressBar(percent, barLen = 40):
    import sys
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "#"
        else:
            progress += "-"
    sys.stdout.write("[%s] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()
