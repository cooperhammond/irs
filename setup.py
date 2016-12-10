from setuptools import setup

setup(
    name='irs',
    version='0.1',
    description='A music downloader that gets metadata.',
    url='http://github.com/kepoorhampond/irs',
    author='Kepoor Hampond',
    author_email='kepoorh@gmail.com',
    license='GNU',
    packages=['irs'],
    install_requires=[
        'youtube-dl',
        'bs4',
        'mutagen',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'irs = irs.__main__:main'
        ]
    },
)
