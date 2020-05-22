require "../bottle/config"

require "./mapper"
require "./song"
require "./list"

class Album < SpotifyList
  @home_music_directory = Config.music_directory

  # Uses the `spotify_searcher` defined in parent `SpotifyList` to find the
  # correct metadata of the list
  def find_it
    album = @spotify_searcher.find_item("album", {
      "name"   => @list_name.as(String),
      "artist" => @list_author.as(String),
    })
    if album
      return album.as(JSON::Any)
    else
      puts "No album was found by that name and artist."
      exit 1
    end
  end

  # Will define specific metadata that may not be included in the raw return
  # of spotify's album json. Moves the title of the album and the album art
  # to the json of the single song
  def organize_song_metadata(list : JSON::Any, datum : JSON::Any) : JSON::Any
    album_metadata = parse_to_json(%(
      {
        "name": "#{list["name"]}",
        "images": [{"url": "#{list["images"][0]["url"]}"}]
      }
    ))

    prepped_data = TrackMapper.from_json(datum.to_json)
    prepped_data.album = album_metadata

    data = parse_to_json(prepped_data.to_json)

    return data
  end

  private def organize(song : Song)
    song.organize_it(@home_music_directory)
  end
end
