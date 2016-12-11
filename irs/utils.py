def strip_special_chars(string):
    special_chars = "\ / : * ? \" < > | - ( )".split(" ")
    for char in special_chars:
        string.replace(char, "")
    return string

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

def color(text, colors=[]):
    color_string = ""
    for color in colors:
        color_string += "bc.%s + " % color
    color_string = color_string[:-2]
    return (eval(color_string) + text + bc.ENDC)
