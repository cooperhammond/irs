from setuptools import setup

setup(
    name =         'irs',
    version =      '7.0.2',
    description =  'A music downloader that gets metadata too.',
    url =          'https://github.com/kepoorhampond/irs',
    author =       'Kepoor Hampond',
    author_email = 'kepoorh@gmail.com',
    license =      'GPL',
    packages =     ['irs', 'irs.search', 'irs.interact', 'irs.glue', 
        'irs.install', 'irs.cli'],
    install_requires = [
        'bs4',          # HTML parsing
        'mutagen',      # MP3 tags
        'argparse',     # CLI arg parsing
        'spotipy',      # Interfacing w/ Spotify API
        'ydl-binaries', # Downloading ffmpeg/ffprobe binaries
        'pyyaml',       # Config files done simply
        'youtube-dl'    # Download youtube videos
    ],
    entry_points = {
        'console_scripts': ['irs = irs.cli.cli:main'],
    },
)
