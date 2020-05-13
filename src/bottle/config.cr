require "yaml"

require "./styles"

EXAMPLE_CONFIG = <<-EOP
#{Style.dim "exampleconfig.yml"}
#{Style.dim "===="}
binary_directory: ~/.irs/bin
music_directory: ~/Music
client_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
client_secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
single_folder_playlist: 
  enabled: true
  retain_playlist_order: true
  overwrite_album: false
#{Style.dim "===="}
EOP

module Config
  extend self

  @@arguments = [
    "binary_directory",
    "music_directory",
    "client_key",
    "client_secret",
    "single_folder_playlist: enabled",
    "single_folder_playlist: retain_playlist_order",
    "single_folder_playlist: overwrite_album",
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

  def overwrite_album? : Bool
    return @@conf["single_folder_playlist"]["overwrite_album"].as_bool
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
