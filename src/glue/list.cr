require "json"

require "../search/spotify"
require "../search/youtube"

require "../interact/ripper"
require "../interact/tagger"

require "./song"

# A parent class for downloading albums and playlists from spotify
abstract class SpotifyList
  @spotify_searcher = SpotifySearcher.new
  @file_names = [] of String

  @outputs : Hash(String, Array(String)) = {
    "searching" => [
      Style.bold("Searching for %l by %a ... \r"),
      Style.green("+ ") + Style.bold("%l by %a                                 \n")
    ],
    "url" => [
      Style.bold("When prompted for a URL, provide a youtube URL or press enter to scrape for one\n")
    ]
  }

  def initialize(@list_name : String, @list_author : String?)
  end

  # Finds the list, and downloads all of the songs using the `Song` class
  def grab_it(flags = {} of String => String)
    ask_url = flags["url"]?
    ask_skip = flags["ask_skip"]?
    is_playlist = flags["playlist"]?
  
    if !@spotify_searcher.authorized?
      raise("Need to call provide_client_keys on Album or Playlist class.")
    end

    if ask_url
      outputter("url", 0)
    end

    outputter("searching", 0)
    list = find_it()
    outputter("searching", 1)
    contents = list["tracks"]["items"].as_a

    i = 0
    contents.each do |datum|
      i += 1
      if datum["track"]?
        datum = datum["track"]
      end

      data = organize_song_metadata(list, datum)

      s_name = data["name"].to_s
      s_artist = data["artists"][0]["name"].to_s

      song = Song.new(s_name, s_artist)
      song.provide_spotify(@spotify_searcher)
      song.provide_metadata(data)

      puts Style.bold("[#{i}/#{contents.size}]")

      unless ask_skip && skip?(s_name, s_artist, is_playlist)
        song.grab_it(flags: flags)
        organize(song)
      else
        puts "Skipping..."
      end
    end
  end

  # Will authorize the class associated `SpotifySearcher`
  def provide_client_keys(client_key : String, client_secret : String)
    @spotify_searcher.authorize(client_key, client_secret)
  end

  private def skip?(name, artist, is_playlist)
    print "Skip #{Style.blue name}" +
      (is_playlist ? " (by #{Style.green artist})": "") + "? "
    response = gets
    return response && response.lstrip.downcase.starts_with? "y"
  end

  private def outputter(key : String, index : Int32)
    text = @outputs[key][index]
      .gsub("%l", @list_name)
      .gsub("%a", @list_author)
    print text
  end

  # Defined in subclasses, will return the appropriate information or call an
  # error if the info is not found and exit
  abstract def find_it : JSON::Any

  # If there's a need to organize the individual song data so that the `Song`
  # class can better handle it, this function will be defined in the subclass
  private abstract def organize_song_metadata(list : JSON::Any,
                                              datum : JSON::Any) : JSON::Any

  # Will define the specific type of organization for a list of songs.
  # Needed because most people want albums sorted by artist, but playlists all
  # in one folder
  private abstract def organize(song : Song)
end
