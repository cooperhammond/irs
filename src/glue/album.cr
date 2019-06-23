require "./song"
require "./list"


class Album < SpotifyList

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

  private def set_organization(index : Int32, song : Song)
    # pass
  end
end

puts Album.new("A Night At The Opera", "Queen").find_it()