import sys

def strip_special_chars(string):
    special_chars = "\ / : * ? \" < > | - ( )".split(" ")
    for char in special_chars:
        string.replace(char, "")
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
