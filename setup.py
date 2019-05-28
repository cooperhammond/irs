from setuptools import setup

setup(
    name =         'irs',
    version =      '7.0.0',
    description =  'A music downloader that gets metadata too.',
    url =          'https://github.com/kepoorhampond/irs',
    author =       'Kepoor Hampond',
    author_email = 'kepoorh@gmail.com',
    license =      'GPL',
    packages =     ['irs', 'irs.search', 'irs.interact', 'irs.glue'],
    install_requires = [
        'bs4',
        'mutagen',
        'argparse'
        'spotipy',
        'ydl-binaries',
    ],
    entry_points = {
        'console_scripts': ['irs = irs.glue.cli:main'],
    },
)
