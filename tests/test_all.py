from os import system, chdir
chdir("tests/")

system("python album.py")
system("python playlist.py")
system("python post_processors.py")
system("python song.py")