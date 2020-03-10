require "../bottle/config"

require "./song"
require "./list"


class Album < SpotifyList

  @music_directory = Config.music_directory

  # Uses the `spotify_searcher` defined in parent `SpotifyList` to find the
  # correct metadata of the list 
  def find_it
    album = @spotify_searcher.find_item("album", {
      "name" => @list_name.as(String),
      "artist" => @list_author.as(String)
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
      json_string = %(
        {
          "album": {
            "name": "#{list["name"]}",
            "images": [{"url": "#{list["images"][0]["url"]}"}]
          },
      )
      datum.as_h.keys.each_with_index do |key, index|
        value = datum[key]
        if value.as_s?
          json_string += %("#{key}": "#{datum[key]}")
        else
          json_string += %("#{key}": #{datum[key].to_s.gsub(" => ", ": ")})
        end

        if index != datum.as_h.keys.size - 1
          json_string += ",\n"
        end
      end
      json_string += %(
        }
      )

      json_string = json_string.gsub("  ", "")
      json_string = json_string.gsub("\n", " ")
      json_string = json_string.gsub("\t", "")

      data = JSON.parse(json_string)

      return data
  end

  private def organize(song : Song)
    song.organize_it(@music_directory)
  end
end
