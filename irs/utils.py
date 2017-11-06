# _*_ coding:utf-8 _*_


# =======
# Imports
# =======

# Static Method Hook
import inspect

# And Now For Something Completely Different
import os
import sys
import re
from time import sleep
import pkg_resources

# Config File and Flags
if sys.version_info[0] == 2:
    import config
    CONFIG = config.CONFIG
else:
    from irs.config import CONFIG


# ==================
# Static Method Hook
# ==================

def staticmethods(cls):
    for name, method in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, staticmethod(method.__func__))
    return cls


# =========================
# Youtube-DL Logs and Hooks
# =========================

@staticmethods
class YdlUtils:
    def clear_line():
        sys.stdout.write("\x1b[2K\r")

    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print(CONFIG["converting"])


# ================================
# Object Manipulation and Checking
# ================================

def set_encoding(ld, encoding):  # ld => list or dictionary with strings in it
    if type(ld) == dict:
        for k in ld:
            if type(ld[k]) == dict or type(ld[k]) == list:
                ld[k] = set_encoding(ld[k], encoding)
            elif type(ld[k]) == str:
                ld[k] = encoding(ld[k])
    elif type(ld) == list:
        for index, datum in enumerate(ld):
            if type(datum) == str:
                ld[index] = encoding(datum)
            elif type(ld[k]) == dict or type(ld[k]) == list:
                ld[k] = set_encoding(ld[k], encoding)
    return ld


@staticmethods
class ObjManip:  # Object Manipulation
    def limit_song_name(song):
        bad_phrases = "remaster  remastered  master".split("  ")
        # I have "master" here because Spotify actually sometimes mispells
        # stuff and it is hella annoying, so this was my solution
        for phrase in bad_phrases:
            if ObjManip.blank_include(song.split(" - ")[-1], phrase):
                return song.split(" - ")[0]
        return song

    def check_garbage_phrases(phrases, string, title):
        for phrase in phrases:
            if phrase in string.lower():
                if phrase not in title.lower():
                    return True
        return False

    def blank(string, downcase=True, remove_and=True):
        if downcase:
            string = string.lower()
        if remove_and:
            string = string.replace("and", "")
        import re
        regex = re.compile('[^a-zA-Z0-9\ ]')
        if sys.version_info == 2:
            string = regex.sub('', string.decode("utf8"))
            return ' '.join(string.decode().split())
        else:
            string = regex.sub('', string)
            return ' '.join(string.split())

    def blank_include(this, includes_this):
        this = ObjManip.blank(this)
        includes_this = ObjManip.blank(includes_this)
        if includes_this in this:
            return True
        return False

    def individual_word_match(match_against, match):
        match_against = ObjManip.blank(match_against).split(" ")
        match = ObjManip.blank(match).split(" ")
        matched = []
        for match_ag in match_against:
            for word in match:
                if match_ag == word:
                    matched.append(word)
        return (float(len(set(matched))) / float(len(match_against)))

    def flatten(l):
        flattened_list = []
        for x in l:
            if type(x) != str:
                for y in x:
                    flattened_list.append(y)
            else:
                flattened_list.append(x)
        return flattened_list

    def remove_none_values(d):
        new_d = d
        for x in list(d.keys()):
            if type(new_d[x]) is list:
                new_d[x] = ObjManip.remove_none_values(d[x])
            elif new_d[x] is None:
                del new_d[x]
        return new_d

    # ld => a list or dictionary with strings in it
    def set_utf8_encoding(ld):
        return set_encoding(ld, lambda x: x.encode('utf-8'))

    def set_encoding(*args):
        return set_encoding(*args)

# ========================================
# Download Log Reading/Updating/Formatting
# ========================================


@staticmethods
class DLog:
    def format_download_log_line(t, download_status="not downloaded"):
        return (" @@ ".join([t["name"], t["artist"], t["album"]["id"],
                str(t["genre"]), t["track_number"], t["disc_number"],
                t["compilation"], t["file_prefix"], download_status]))

    def format_download_log_data(data):
        lines = []
        for track in data:
            lines.append(DLog.format_download_log_line(track))
        return "\n".join(lines)

    def read_download_log(spotify):
        data = []
        with open(".irs-download-log", "r") as file:
            for line in file:
                line = line.split(" @@ ")
                data.append({
                    "name":          line[0],
                    "artist":        line[1],
                    "album":         spotify.album(line[2]),
                    "genre":         eval(line[3]),
                    "track_number":  line[4],
                    "disc_number":   line[5],
                    "compilation":   bool(line[6]),
                    "file_prefix":   line[7],
                })
        return data

    def update_download_log_line_status(track, status="downloaded"):
        line_to_find = DLog.format_download_log_line(track)
        with open(".irs-download-log", "r") as input_file:
            with open(".irs-download-log", "w") as output_file:
                for line in input_file:
                    if line == line_to_find:
                        output_file.write(
                            DLog.format_download_log_line(track, status))
                    else:
                        output_file.write(line)


# ===========================================
# And Now, For Something Completely Different
# ===========================================
#              (It's for the CLI)

try:
    COLS = int(os.popen('tput cols').read().strip("\n"))
except:
    COLS = 80

if sys.version_info[0] == 2:
    def input(string):
        return raw_input(string)


def code(code1):
    return "\x1b[%sm" % str(code1)


def no_colors(string):
    return re.sub("\x1b\[\d+m", "", string)


def center_colors(string, cols):
    return no_colors(string).center(cols).replace(no_colors(string), string)


def decode_utf8(string):
    if sys.version_info[0] == 3:
        return string.encode("utf8", "strict").decode()
    elif sys.version_info[0] == 2:
        return string.decode("utf8")


def center_unicode(string, cols):
    tmp_chars = "X" * len(decode_utf8(string))
    chars = center_colors(tmp_chars, cols)
    return chars.replace(tmp_chars, string)


def center_lines(string, cols, end="\n"):
    lines = []
    for line in string.split("\n"):
        lines.append(center_unicode(line, cols))
    return end.join(lines)


def flush_puts(msg, time=0.01):
    # For slow *burrrp* scroll text, Morty. They-They just love it, Morty.
    # When they see this text. Just slowwwly extending across the page. Mmm,
    # mmm. You just give the time for how *buurp* slow you wa-want it, Morty.
    # It works with colors and escape characters too, Morty.
    # Your grandpa's a genius *burrrp* Morty
    def check_color(s):
        if "\x1b" not in s:
            new = list(s)
        else:
            new = s
        return new
    msg = re.split("(\x1b\[\d+m)", msg)
    msg = list(filter(None, map(check_color, msg)))
    msg = ObjManip.flatten(msg)
    for char in msg:
        if char not in (" ", "", "\n") and "\x1b" not in char:
            sleep(time)
        sys.stdout.write(char)
        sys.stdout.flush()
    print("")


BOLD = code(1)
END = code(0)
RED = code(31)
GREEN = code(32)
YELLOW = code(33)
BLUE = code(34)
PURPLE = code(35)
CYAN = code(36)
GRAY = code(37)
BRED = RED + BOLD
BGREEN = GREEN + BOLD
BYELLOW = YELLOW + BOLD
BBLUE = BLUE + BOLD
BPURPLE = PURPLE + BOLD
BCYAN = CYAN + BOLD
BGRAY = GRAY + BOLD


def banner():
    title = (BCYAN + center_lines("""\
██╗██████╗ ███████╗
██║██╔══██╗██╔════╝
██║██████╔╝███████╗
██║██╔══██╗╚════██║
██║██║  ██║███████║
╚═╝╚═╝  ╚═╝╚══════╝\
""", COLS) + END)
    for num in range(0, 6):
        os.system("clear || cls")
        if num % 2 == 1:
            print(BRED + center_unicode("🚨   🚨  🚨    🚨  🚨   \r", COLS))
        else:
            print("")
        print(title)
        sleep(0.3)
    flush_puts(center_colors("{0}Ironic Redistribution System ({1}IRS{2})"
                             .format(BYELLOW, BRED, BYELLOW), COLS))

    flush_puts(center_colors("{0}Made with 😈  by: {1}Kepoor Hampond \
({2}kepoorhampond{3})".format(BBLUE, BYELLOW, BRED, BYELLOW) + END, COLS))

    flush_puts(center_colors("{0}Version: {1}".format(BBLUE, BYELLOW) +
               pkg_resources.get_distribution("irs").version, COLS))


def menu(unicode, time=0.01):
    flush_puts("Choose option from menu:", time)
    flush_puts("\t[{0}song{1}] Download Song".format(BGREEN, END), time)
    flush_puts("\t[{0}album{1}] Download Album".format(BGREEN, END), time)
    flush_puts("\t[{0}{1}{2}] Download Playlist"
               .format(BGREEN, unicode[-1], END), time)
    flush_puts("\t[{0}help{1}] Print This Menu".format(BGREEN, END), time)
    flush_puts("\t[{0}exit{1}] Exit IRS".format(BGREEN, END), time)
    print("")


def console(ripper):
    banner()
    print(END)
    if ripper.authorized is True:
        unicode = [BGREEN + "✔" + END, "list"]
    elif ripper.authorized is False:
        unicode = [BRED + "✘" + END]
    flush_puts("[{0}] Authenticated with Spotify".format(unicode[0]))
    print("")
    menu(unicode)
    while True:
        try:
            choice = input("{0}irs{1}>{2} ".format(BBLUE, BGRAY, END))

            if choice in ("exit", "e"):
                raise KeyboardInterrupt

            try:
                if choice in ("song", "s"):
                    song_name = input("Song name{0}:{1} ".format(BBLUE, END))
                    artist_name = input("Artist name{0}:{1} "
                                        .format(BBLUE, END))
                    ripper.song(song_name, artist_name)

                elif choice in ("album", "a"):
                    album_name = input("Album name{0}:{1} ".format(BBLUE, END))
                    ripper.spotify_list("album", album_name)

                elif choice in ("list", "l") and ripper.authorized is True:
                    username = input("Spotify Username{0}:{1} "
                                     .format(BBLUE, END))
                    list_name = input("Playlist Name{0}:{1} "
                                      .format(BBLUE, END))
                    ripper.spotify_list("playlist", list_name, username)

                elif choice in ("help", "h", "?"):
                    menu(unicode, 0)
            except (KeyboardInterrupt, EOFError):
                print("")
                pass

        except (KeyboardInterrupt, EOFError):
            sys.exit(0)


"""
# =====================
# Config File and Flags
# =====================

def check_sources(ripper, key, default=None, environment=False, where=None):
    if where is not None:
        tmp_args = ripper.args.get(where)
    else:
        tmp_args = ripper.args

    if tmp_args.get(key):
        return tmp_args.get(key)
"""


# ===========
# CONFIG FILE
# ===========

def check_sources(ripper, key, default=None, environment=False, where=None):
    # tmp_args = ripper.args
    # if where is not None and ripper.args.get(where):
    #     tmp_args = ripper.args.get("where")

    if ripper.args.get(key):
        return ripper.args.get(key)
    elif CONFIG.get(key):
        return CONFIG.get(key)
    elif os.environ.get(key) and environment is True:
        return os.environ.get(key)
    else:
        return default


@staticmethods
class Config:

    def parse_spotify_creds(ripper):
        CLIENT_ID = check_sources(ripper, "SPOTIFY_CLIENT_ID",
                                  environment=True)
        CLIENT_SECRET = check_sources(ripper, "SPOTIFY_CLIENT_SECRET",
                                      environment=True)
        return CLIENT_ID, CLIENT_SECRET

    def parse_search_terms(ripper):
        search_terms = check_sources(ripper, "additional_search_terms",
                                     "lyrics")
        return search_terms

    def parse_artist(ripper):
        artist = check_sources(ripper, "artist")
        return artist

    def parse_directory(ripper):
        directory = check_sources(ripper, "custom_directory",
                                  where="post_processors")
        if directory is None:
            directory = check_sources(ripper, "custom_directory", "~/Music")
        return directory.replace("~", os.path.expanduser("~"))

    def parse_default_flags(default=""):
        if CONFIG.get("default_flags"):
            args = sys.argv[1:] + CONFIG.get("default_flags")
        else:
            args = default
        return args

    def parse_organize(ripper):
        organize = check_sources(ripper, "organize")
        if organize is None:
            return check_sources(ripper, "organize", False,
                                 where="post_processors")
        else:
            return True

    def parse_exact(ripper):
        exact = check_sources(ripper, "exact")
        if exact in (True, False):
            return exact



#==============
# Captcha Cheat
#==============
# I basically consider myself a genius for this snippet.

from splinter import Browser
from time import sleep


@staticmethods
class CaptchaCheat:
    def cheat_it(url, t=1):
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        with Browser('chrome', **executable_path) as b:
            b.visit(url)
            sleep(t)
            while CaptchaCheat.strip_it(b.evaluate_script("document.URL")) != CaptchaCheat.strip_it(url):
                sleep(t)
            return b.evaluate_script("document.getElementsByTagName('html')[0].innerHTML")

    def strip_it(s):
        s = s.encode("utf-8")
        s = s.strip("http://")
        s = s.strip("https://")
        return s
