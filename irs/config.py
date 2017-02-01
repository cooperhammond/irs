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
    client_id = '',
    client_secret = '',

    additional_search_terms = 'lyrics',

    # For a custom directory. Note that `~` will not work as a shortcut in a
    # plain text manner.
    directory = str(expanduser("~")) + "/Music",

    # If you want numbered file names
    numbered_file_names = True,

    # Downloaded file names
    download_file_names = False,
)
