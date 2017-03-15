from os.path import expanduser

CONFIG = dict(

    # To autostart rhythmbox with a new song:
    # default_flags = '-c rhythmbox %(loc)s',
    # To make choosing of links default:
    # default_flags = '-l',
    # To place all playlist songs into one folder:
    # default_flags = '-of',
    default_flags = '',


    # You can either specify Spotify keys here, or in environment variables.
    SPOTIFY_CLIENT_ID = '',
    SPOTIFY_CLIENT_SECRET = '',

    additional_search_terms = 'lyrics',

    # For a custom directory. Note that `~` will not work as a shortcut in a
    # plain text manner.
    # TODO: Implement this into the utils arguments.
    custom_directory = str(expanduser("~")) + "/Music",
)
