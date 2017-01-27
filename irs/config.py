from os.path import expanduser

CONFIG = dict(

    # To autostart rhythmbox with a new song:
    # default_flags = '-c rhythmbox %(loc)s',
    # To make choosing of links default:
    # default_flags = '-l',
    # To place all playlist songs into one folder:
    # default_flags = '-of',
    default_flags = '',


    # These are necessary to download Spotify playlists
    client_id = 'e4198f6a3f7b48029366f22528b5dc66',
    client_secret = '69adc699f79e4640a6fd7610635b025f',

    # For a custom directory. Note that `~` will not work as a shortcut.
    directory = str(expanduser("~")) + "/Music",

    # If you want numbered file names
    numbered_file_names = True,

    # Downloaded file names
    download_file_names = False,
)
