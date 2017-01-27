CONFIG = dict(

    # To autostart rhythmbox with a new song:
    # default_flags = '-c rhythmbox %(loc)s',
    # To make choosing of links default:
    # default_flags = '-l',
    default_flags = '',


    # These are necessary to download Spotify playlists
    client_id = '',
    client_secret = '',

    # For a custom directory. Note that `~` will not work as a shortcut.
    directory = '',

    # If you want numbered file names
    numbered_file_names = True,

    # Downloaded file names
    download_file_names = True,
)
