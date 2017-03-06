# -*- coding: UTF-8 -*-


#==========================
# Youtube-DL Logs and Hooks
#==========================

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print ("Converting to mp3 ...")


#=================================
# String Manipulation and Checking
#=================================

def check_garbage_phrases(phrases, string, title):
    for phrase in phrases:
        if phrase in blank(string):
            if not phrase in blank(title):
                return True
    return False
        
def blank(string, downcase=True):
    import re
    regex = re.compile('[^a-zA-Z0-9\ ]')
    string = regex.sub('', string)
    if downcase: string = string.lower()
    return string
    
def blank_include(this, includes_this):
    this = blank(this)
    includes_this = blank(includes_this)
    if includes_this in this:
        return True
    return False

def individual_word_match(match_against, match):
    match_against = blank(match_against).split(" ")
    match = blank(match).split(" ")
    matched = []
    for match_ag in match_against:
        for word in match:
            if match_ag == word:
                matched.append(word)
    return (float(matched.uniq.size) / float(match_against.size))

def flatten(l):
    flattened_list = []
    for x in l:
        if type(x) != str:
            for y in x:
                flattened_list.append(y)
        else:
            flattened_list.append(x)
    return flattened_list
    
#=========================================
# Download Log Reading/Updating/Formatting
#=========================================
    
def format_download_log_line(t, download_status="not downloaded"):
    return (" @@ ".join([t["name"], t["artist"], t["album"]["id"], \
    str(t["genre"]), t["track_number"], t["disc_number"], t["compilation"], \
    t["file_prefix"], download_status]))

def format_download_log_data(data):
    lines = []
    for track in data:
        lines.append(format_download_log_line(track))
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
    line_to_find = format_download_log_line(track)
    with open(".irs-download-log", "r") as input_file, \
    open(".irs-download-log", "w") as output_file:
            for line in input_file:
                if line == line_to_find:
                    output_file.write(format_download_log_line(track, status))
                else:
                    output_file.write(line)
                    
                    
#============================================
# And Now, For Something Completely Different
#============================================
#              (It's for the CLI)

import os, sys, re
from time import sleep

COLS = int(os.popen('tput cols').read().strip("\n"))

def code(code1):
    return "\x1b[%sm" % str(code1)
    
def no_colors(string):
    return re.sub("\x1b\[\d+m", "", string)
    
def center_colors(string, cols):
    return no_colors(string).center(cols).replace(no_colors(string), string) 
        
def center_unicode(string, cols):
    tmp_chars = "X" * len(string.decode("utf8"))
    chars = center_colors(tmp_chars, cols)
    return chars.replace(tmp_chars, string)
    
def center_lines(string, cols, end="\n"):
    lines = []
    for line in string.split("\n"):
        lines.append(center_unicode(line, cols))
    return end.join(lines)
    
def flush_puts(msg, time=0.03):
    # For slow *burrrp* scroll text, Morty. They-They just love it, Morty.
    # When they see this text. Just slowwwly extending across the page. Mmm, mmm.
    # You just give the time for how *buurp* slow you wa-want it, Morty.
    # It works with colors and escape characters too, Morty. 
    # Your grandpa's a genius *burrrp* Morty
    pattern = re.compile("(\x1b\[\d+m)")
    def check_color(s):
        if "\x1b" not in s:
            new = list(s)
        else:
            new = s
        return new
    msg = re.split("(\x1b\[\d+m)", msg)
    msg = list(filter(None, map(check_color, msg)))
    msg = flatten(msg)
    for char in msg:
        if char not in (" ", "", "\n") and "\x1b" not in char:
            sleep(time)
        sys.stdout.write(char)
        sys.stdout.flush()
    print ("")
    

BOLD = code(1)
END = code(0)
RED = code(31)
GREEN = code(32)
YELLOW = code(33)
BLUE = code(34)
PURPLE = code(35)
CYAN = code(36)
BRED = RED + BOLD
BGREEN = GREEN + BOLD
BYELLOW = YELLOW + BOLD
BBLUE = BLUE + BOLD
BPURPLE = PURPLE + BOLD
BCYAN = CYAN + BOLD


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
            print (BRED + center_unicode("🚨   🚨  🚨    🚨  🚨   \r", COLS))
        else:
            print ("")
        print (title)
        sleep(0.3)
    flush_puts(center_colors(BYELLOW + "\
Ironic Redistribution System (" + BRED + "IRS" + BYELLOW + ")" + END, COLS))
    flush_puts(center_colors(BBLUE + "\
Made with 😈  by: " + BYELLOW + "Kepoor Hampond (" + BRED + \
"kepoorhampond" + BYELLOW + ")" + END, COLS))