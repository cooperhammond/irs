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