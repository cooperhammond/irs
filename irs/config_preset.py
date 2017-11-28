CONFIG = dict(

    # For default flags. Right now, it organizes your files into an
    # artist/album/song structure.
    # To add a flag or argument, add an element to the index:
    # default_flags = ['-o', '-l', '~/Music']xs
    default_flags = ['-o'],

    # You can either specify Spotify keys here, or in environment variables.
    SPOTIFY_CLIENT_ID = '',
    SPOTIFY_CLIENT_SECRET = '',

    # Search terms for youtube
    additional_search_terms = 'lyrics',

    # True always forces organization.
    # False always forces non-organization.
    # None allows options and flags to determine if the files
    # will be organized.
    organize = True,

    # When blank, defaults to '~/Music'
    custom_directory = "",

    # For fancy printing with draftlog
    fancy_printing = True,
)
