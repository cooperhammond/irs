from os import system
from sys import exit
from .manage import *
from .utils import *

class Manager:
    def __init__(self, args):
        self.args = args

    def main():
        args = self.a

        if args.version:
            import pkg_resources
            print ("\n\n" + color("Ingenious Redistribution System", ["HEADER", "BOLD"]))
            print ("Homepage: " + color("https://github.com/kepoorhampond/irs", ["OKGREEN"]))
            print ("License: " + color("The GNU", ["YELLOW"]) + " (http://www.gnu.org/licenses/gpl.html)")
            print ("Version: " + pkg_resources.get_distribution("irs").version)
            print ("\n")
            exit(0)

        elif not args.album and args.search_terms:
            parser.error("error: must supply -A/--album if you are going to supply -st/--search-terms")
            exit(1)

        elif args.artist and not (args.album or args.song):
            print ("error: must specify -A/--album or -s/--song if specifying -a/--artist")
            exit(1)

        elif not args.artist and not args.playlist:
            console(args)

        elif args.playlist:
            rip_playlist(args.playlist, args.command, choose_link=args.link, no_organize=args.no_organize)

        elif args.artist:
            if args.album:
                rip_album(args.album, args.artist, command=args.command, \
                    search=args.search_terms, choose_link=args.link)

            elif args.song:
                rip_mp3(args.song, args.artist, command=args.command, choose_link=args.link)
