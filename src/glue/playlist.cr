require "../bottle/config"

require "./song"
require "./list"

class Playlist < SpotifyList

  @home_music_directory = Config.music_directory

  # Uses the `spotify_searcher` defined in parent `SpotifyList` to find the
  # correct metadata of the list 
  def find_it
    @playlist = @spotify_searcher.find_item("playlist", {
      "name" => @list_name.as(String),
      "username" => @list_author.as(String)
    })
    if playlist
      return playlist.as(JSON::Any)
    else
      puts "No playlists were found by that name and user."
      exit 1
    end
  end

  # Will define specific metadata that may not be included in the raw return 
  # of spotify's album json. Moves the title of the album and the album art
  # to the json of the single song
  def organize_song_metadata(list : JSON::Any, datum : JSON::Any) : JSON::Any
    puts datum
    puts "THIS"

    exit 0
    data = datum

    return data
  end

  private def organize(song : Song)
    song.organize_it(@home_music_directory)
  end
end
