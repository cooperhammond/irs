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
    
def format_download_log_line(track, download_status="not downloaded"):
    return " @@ ".join([t["name"], t["artist"], t["album"]["id"], \
    t["genre"], t["track_number"], t["disc_number"], t["compilation"], \
    t["prefix"], download_status]) + "\n"

def format_download_log_data(data):
    line = []
    for track in data:
        lines.append(format_download_log_line(track))
    return lines
    
def update_download_log_line_status(track, status="downloaded"):
    line_to_find = format_download_log_line(track)
    with open(".irs-download-log", "r") as input_file, \
    open(".irs-download-log", "w") as output_file:
            for line in input_file:
                if line == line_to_find:
                    output_file.write(format_download_log_line(track, status))
                else:
                    output_file.write(line)
            