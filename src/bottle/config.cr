require "yaml"

require "./styles"

require "../search/spotify"

EXAMPLE_CONFIG = <<-EOP
#{Style.dim "exampleconfig.yml"}
#{Style.dim "===="}
#{Style.blue "binary_directory"}: #{Style.green "~/.irs/bin"}
#{Style.blue "music_directory"}: #{Style.green "~/Music"}
#{Style.blue "filename_pattern"}: #{Style.green "\"{track_number} - {title}\""}
#{Style.blue "directory_pattern"}: #{Style.green "\"{artist}/{album}\""}
#{Style.blue "client_key"}: #{Style.green "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}
#{Style.blue "client_secret"}: #{Style.green "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}
#{Style.blue "single_folder_playlist"}: 
  #{Style.blue "enabled"}: #{Style.green "true"}
  #{Style.blue "retain_playlist_order"}: #{Style.green "true"}
  #{Style.blue "unify_into_album"}: #{Style.green "false"}
#{Style.dim "===="}
EOP

module Config
  extend self

  @@arguments = [
    "binary_directory",
    "music_directory",
    "filename_pattern",
    "directory_pattern",
    "client_key",
    "client_secret",
    "single_folder_playlist: enabled",
    "single_folder_playlist: retain_playlist_order",
    "single_folder_playlist: unify_into_album",
  ]

  @@conf = YAML.parse("")
  begin
    @@conf = YAML.parse(File.read(ENV["IRS_CONFIG_LOCATION"]))
  rescue
    puts Style.red "Before anything else, define the environment variable IRS_CONFIG_LOCATION pointing to a .yml file like this one."
    puts EXAMPLE_CONFIG
    puts Style.bold "See https://github.com/cooperhammond/irs for more information on the config file"
    exit 1
  end

  def binary_location : String
    path = @@conf["binary_directory"].to_s
    return Path[path].expand(home: true).to_s
  end

  def music_directory : String
    path = @@conf["music_directory"].to_s
    return Path[path].expand(home: true).to_s
  end
  
  def filename_pattern : String
    return @@conf["filename_pattern"].to_s
  end
  
  def directory_pattern : String
    return @@conf["directory_pattern"].to_s
  end

  def client_key : String
    return @@conf["client_key"].to_s
  end

  def client_secret : String
    return @@conf["client_secret"].to_s
  end

  def single_folder_playlist? : Bool
    return @@conf["single_folder_playlist"]["enabled"].as_bool
  end

  def retain_playlist_order? : Bool
    return @@conf["single_folder_playlist"]["retain_playlist_order"].as_bool
  end

  def unify_into_album? : Bool
    return @@conf["single_folder_playlist"]["unify_into_album"].as_bool
  end

  def check_necessities
    missing_configs = [] of String
    @@arguments.each do |argument|
      if !check_conf(argument)
        missing_configs.push(argument)
      end
    end
    if missing_configs.size > 0
      puts Style.red("You are missing the following key(s) in your YAML config file:")
      missing_configs.each do |config|
        puts "  " + config
      end
      puts "\nHere's an example of what your config should look like:"
      puts EXAMPLE_CONFIG
      puts Style.bold "See https://github.com/cooperhammond/irs for more information on the config file"
      exit 1
    end
    spotify = SpotifySearcher.new
    spotify.authorize(self.client_key, self.client_secret)
    if !spotify.authorized?
      puts Style.red("There's something wrong with your client key and/or client secret")
      puts "Get your keys from https://developer.spotify.com/dashboard, and enter them in your config file"
      puts "Your config file is at #{ENV["IRS_CONFIG_LOCATION"]}"
      puts EXAMPLE_CONFIG
      puts Style.bold "See https://github.com/cooperhammond/irs for more information on the config file"
      exit 1
    end
  end

  private def check_conf(key : String) : YAML::Any?
    if key.includes?(": ")
      args = key.split(": ")
      if @@conf[args[0]]?
        return @@conf[args[0]][args[1]]?
      else
        return @@conf[args[0]]?
      end
    else
      return @@conf[key]?
    end
  end
end
