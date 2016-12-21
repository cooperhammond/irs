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
