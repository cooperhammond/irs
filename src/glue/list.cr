require "../search/spotify"
require "../search/youtube"

require "../interact/ripper"
require "../interact/tagger"

require "./song"


# A parent class for downloading albums and playlists from spotify
abstract class SpotifyList
  @spotify_searcher = SpotifySearcher.new()
  @file_names = [] of String

  def initialize(@list_name : String, @list_author : String?)
    @spotify_searcher.authorize(
      "e4198f6a3f7b48029366f22528b5dc66", 
      "ba057d0621a5496bbb64edccf758bde5")
  end

  # Finds the list, and downloads all of the songs using the `Song` class
  def grab_it
    list = find_it()
    contents = list["tracks"][0]["items"]

    i = 0
    contents.each do |data|
      if song["track"]?
        data = data["track"]
      end

      song = Song.new(data["name"].to_s, data["artists"][0]["name"].to_s)
      song.provide_spotify(@spotify_searcher)
      set_organization(i , song)
      song.grab_it()

      i += 1
    end
  end

  abstract def find_it : JSON::Any

  private abstract def set_organization(song_index : Int32, song : Song)

end