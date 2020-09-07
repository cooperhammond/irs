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
  def grab_it(ask_url : Bool = false)
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
      if datum["track"]?
        datum = datum["track"]
      end

      data = organize_song_metadata(list, datum)

      song = Song.new(data["name"].to_s, data["artists"][0]["name"].to_s)
      song.provide_spotify(@spotify_searcher)
      song.provide_metadata(data)

      puts Style.bold("[#{data["track_number"]}/#{contents.size}]")
      song.grab_it ask_url: ask_url

      organize(song)

      i += 1
    end
  end

  # Will authorize the class associated `SpotifySearcher`
  def provide_client_keys(client_key : String, client_secret : String)
    @spotify_searcher.authorize(client_key, client_secret)
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
