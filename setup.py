from setuptools import setup

setup(
    name =         'irs',
    version =      '6.7.7',
    description =  'A music downloader that just gets metadata.',
    url =          'https://github.com/kepoorhampond/irs',
    author =       'Kepoor Hampond',
    author_email = 'kepoorh@gmail.com',
    license =      'GPL',
    packages =     ['irs'],
    install_requires = [
        'bs4',
        'mutagen',
        'requests',
        'spotipy',
        'ydl-binaries',
        'splinter'
    ],
    entry_points = {
        'console_scripts': ['irs = irs.cli:main'],
    },
)
