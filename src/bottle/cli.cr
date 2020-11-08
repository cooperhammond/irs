require "ydl_binaries"

require "./config"
require "./styles"
require "./version"

require "../glue/song"
require "../glue/album"
require "../glue/playlist"

class CLI
  # layout:
  # [[shortflag, longflag], key, type]
  @options = [
    [["-h", "--help"], "help", "bool"],
    [["-v", "--version"], "version", "bool"],
    [["-i", "--install"], "install", "bool"],
    [["-c", "--config"], "config", "bool"],
    [["-a", "--artist"], "artist", "string"],
    [["-s", "--song"], "song", "string"],
    [["-A", "--album"], "album", "string"],
    [["-p", "--playlist"], "playlist", "string"],
    [["-u", "--url"], "url", "string"],
    [["-g", "--give-url"], "give-url", "bool"],
  ]

  @args : Hash(String, String)

  def initialize(argv : Array(String))
    @args = parse_args(argv)
  end

  def version
    puts "irs v#{IRS::VERSION}"
  end

  def help
    msg = <<-EOP
    #{Style.bold "Usage: irs [--help] [--version] [--install]"}
    #{Style.bold "           [-s <song> -a <artist>]"}
    #{Style.bold "           [-A <album> -a <artist>]"}
    #{Style.bold "           [-p <playlist> -a <username>]"}

    #{Style.bold "Arguments:"}
        #{Style.blue "-h, --help"}                  Show this help message and exit
        #{Style.blue "-v, --version"}               Show the program version and exit
        #{Style.blue "-i, --install"}               Download binaries to config location
        #{Style.blue "-c, --config"}                Show config file location
        #{Style.blue "-a, --artist <artist>"}       Specify artist name for downloading
        #{Style.blue "-s, --song <song>"}           Specify song name to download
        #{Style.blue "-A, --album <album>"}         Specify the album name to download
        #{Style.blue "-p, --playlist <playlist>"}   Specify the playlist name to download
        #{Style.blue "-u, --url <url>"}             Specify the youtube url to download from (for single songs only)
        #{Style.blue "-g, --give-url"}              Specify the youtube url sources while downloading (for albums or playlists only)

    #{Style.bold "Examples:"}
        $ #{Style.green %(irs --song "Bohemian Rhapsody" --artist "Queen")}
        #{Style.dim %(# => downloads the song "Bohemian Rhapsody" by "Queen")}
        $ #{Style.green %(irs --album "Demon Days" --artist "Gorillaz")}
        #{Style.dim %(# => downloads the album "Demon Days" by "Gorillaz")}
        $ #{Style.green %(irs --playlist "a different drummer" --artist "prakkillian")}
        #{Style.dim %(# => downloads the playlist "a different drummer" by the user prakkillian)}

    #{Style.bold "This project is licensed under the MIT license."}
    #{Style.bold "Project page: <https://github.com/cooperhammond/irs>"}
    EOP

    puts msg
  end

  def act_on_args
    Config.check_necessities

    if @args["help"]? || @args.keys.size == 0
      help
    elsif @args["version"]?
      version
    elsif @args["install"]?
      YdlBinaries.get_both(Config.binary_location)
    elsif @args["config"]?
      puts ENV["IRS_CONFIG_LOCATION"]?
    elsif @args["song"]? && @args["artist"]?
      s = Song.new(@args["song"], @args["artist"])
      s.provide_client_keys(Config.client_key, Config.client_secret)
      s.grab_it(@args["url"]?)
      s.organize_it(Config.music_directory)
    elsif @args["album"]? && @args["artist"]?
      a = Album.new(@args["album"], @args["artist"])
      a.provide_client_keys(Config.client_key, Config.client_secret)
      if @args["give-url"]?
        a.grab_it(true)
      else
        a.grab_it(false)
      end
    elsif @args["playlist"]? && @args["artist"]?
      p = Playlist.new(@args["playlist"], @args["artist"])
      p.provide_client_keys(Config.client_key, Config.client_secret)
      if @args["give-url"]?
        p.grab_it(true)
      else
        p.grab_it(false)
      end
    else
      puts Style.red("Those arguments don't do anything when used that way.")
      puts "Type `irs -h` to see usage."
    end
  end

  private def parse_args(argv : Array(String)) : Hash(String, String)
    arguments = {} of String => String

    i = 0
    current_key = ""
    pass_next_arg = false
    argv.each do |arg|
      # If the previous arg was an arg flag, this is an arg, so pass it
      if pass_next_arg
        pass_next_arg = false
        i += 1
        next
      end

      flag = [] of Array(String) | String
      valid_flag = false

      @options.each do |option|
        if option[0].includes?(arg)
          flag = option
          valid_flag = true
          break
        end
      end

      # ensure the flag is actually defined
      if !valid_flag
        arg_error argv, i, %("#{arg}" is an invalid flag or argument.)
      end

      # ensure there's an argument if the program needs one
      if flag[2] == "string" && i + 1 >= argv.size
        arg_error argv, i, %("#{arg}" needs an argument.)
      end

      key = flag[1].as(String)
      if flag[2] == "string"
        arguments[key] = argv[i + 1]
        pass_next_arg = true
      elsif flag[2] == "bool"
        arguments[key] = "true"
      end

      i += 1
    end

    return arguments
  end

  private def arg_error(argv : Array(String), arg : Int32, msg : String) : Nil
    precursor = "irs"

    precursor += " " if arg != 0

    if arg == 0
      start = [] of String
    else
      start = argv[..arg - 1]
    end
    last = argv[arg + 1..]

    distance = (precursor + start.join(" ")).size

    print Style.dim(precursor + start.join(" "))
    print Style.bold(Style.red(" " + argv[arg]).to_s)
    puts Style.dim (" " + last.join(" "))

    (0..distance).each do |i|
      print " "
    end
    puts "^"

    puts Style.red(Style.bold(msg).to_s)
    puts "Type `irs -h` to see usage."
    exit 1
  end
end
