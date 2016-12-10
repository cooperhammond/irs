def strip_special_chars(string):
    special_chars = "\ / : * ? \" < > | - ( )".split(" ")
    for char in special_chars:
        string.replace(char, "")
    return string

def color(text, type):
    types = {'HEADER': '\033[95m', 'OKBLUE': '\033[94m', 'OKGREEN': '\033[92m',
    'WARNING': '\033[93m','FAIL': '\033[91m','ENDC': '\033[0m','BOLD': '\033[1m'
    ,'UNDERLINE': '\033[4m'}
    return types[type] + text + types['ENDC']
