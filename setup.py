from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # Actually install the module and dependencies

        try:
            import ydl_binaries
        except ImportError:
            import pip
            pip.main(['install', "ydl-binaries"])

        import ydl_binaries
        from os import path
        from shutil import copyfile

        print("\n\nDownloading Dependencies:\n")
        ydl_binaries.download_ffmpeg("~/.irs/bin")
        ydl_binaries.update_ydl("~/.irs/bin")

        config_file = path.expanduser("~/.irs/config_.py")
        if not path.isfile(config_file):
            copyfile("irs/config_preset", config_file)


setup(
    name =         'irs',
    version =      '6.6.0',
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
        'ydl-binaries'
    ],
    entry_points = {
        'console_scripts': ['irs = irs.cli:main'],
    },
    cmdclass = {
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
