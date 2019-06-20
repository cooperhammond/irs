require "http"
require "json"
require "base64"


class SpotifySearcher
  @root_url = Path["https://api.spotify.com/v1/"]

  @access_header : (HTTP::Headers | Nil) = nil
  @authorized = false

  # Saves an access token for future program use with spotify using client IDs.
  # Specs defined on spotify's developer api: 
  # https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
  #
  # ```
  # SpotifySearcher.new().authorize("XXXXXXXXXX", "XXXXXXXXXX")
  # ```
  def authorize(client_id : String, client_secret : String) : self
    auth_url = "https://accounts.spotify.com/api/token"

    headers = HTTP::Headers{
      "Authorization" => "Basic " + 
        Base64.strict_encode "#{client_id}:#{client_secret}"
    }

    payload = "grant_type=client_credentials"

    response = HTTP::Client.post(auth_url, headers: headers, form: payload)
    error_check(response)

    access_token = JSON.parse(response.body)["access_token"]
    
    @access_header = HTTP::Headers{
      "Authorization" => "Bearer #{access_token}"
    }

    @authorized = true

    return self
  end

  # Check if the class is authorized or not
  def authorized? : Bool
    return @authorized
  end

  # Searches spotify with the specified parameters for the specified items
  #
  # ```
  # spotify_searcher.find_item("track", {
  #   "artist" => "Queen",
  #   "track" => "Bohemian Rhapsody"
  # })
  # => {track metadata}
  # ```
  def find_item(item_type : String, item_parameters : Hash, offset=0, 
  limit=20) : JSON::Any?

    query = generate_query(item_type, item_parameters, offset, limit)

    url = @root_url.join("search?q=#{query}").to_s()

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)

    items = JSON.parse(response.body)[item_type + "s"]["items"].as_a

    points = rank_items(items, item_parameters)

    begin
      return items[points[0][1]]
    rescue IndexError
      return nil
    end
  end

  # Find the genre of an artist based off of their id
  #
  # ```
  # SpotifySearcher.new().authorize(...).find_genre("1dfeR4HaWDbWqFHLkxsg1d")
  # ```
  def find_genre(id : String) : String
    url = @root_url.join("artists/#{id}").to_s()

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)

    genre = JSON.parse(response.body)["genres"][0].to_s
    genre = genre.split(" ").map { |x| x.capitalize }.join(" ")

    return genre
  end

  # Checks for errors in HTTP requests and raises one if found
  private def error_check(response : HTTP::Client::Response) : Nil
    if response.status_code != 200
      raise("There was an error with your request.\n" +
            "Status code: #{response.status_code}\n" + 
            "Response: \n#{response.body}")
    end
  end
  
  # Generates url to run a GET request against to the Spotify open API
  # Returns a `String.`
  private def generate_query(item_type : String, item_parameters : Hash,
  offset : Int32, limit : Int32) : String
    query = ""

    # parameter keys to exclude in the api request. These values will be put
    # in, just not their keys.
    query_exclude = ["username"]

    item_parameters.keys.each do |k|
      # This will map album, playlist, and track from the name key to the query
      if k == "name"
        query += param_encode(item_type, item_parameters[k])

      # check if the key is to be excluded
      elsif !query_exclude.includes?(k)
        query += item_parameters[k].gsub(" ", "+") + "+"

      # if it's none of the above, treat it normally
      else
        query += param_encode(k, item_parameters[k])
      end
    end

    # extra api info
    query += "&type=#{item_type}&offset=#{offset}&limit=#{limit}"

    return query
  end

  # Ranks the given items based off of the info from parameters.
  # Meant to find the item that the user desires.
  # Returns an `Array` of `Array(Int32)` or [[3, 1], [...], ...]
  private def rank_items(items : Array,
  parameters : Hash) : Array(Array(Int32))
    points = [] of Array(Int32)
    index = 0

    items.each do |item|
      pts = 0

      # Think about whether this following logic is worth having in one method.
      # Is it nice to have a single method that handles it all or having a few
      # methods for each of the item types? (track, album, playlist)
      parameters.keys.each do |k| 
        val = parameters[k]

        # The key to compare to for artist
        if k == "artist"
          pts += points_compare(item["artists"][0]["name"].to_s, val)
        end

        # The key to compare to for playlists
        if k == "username"
          pts += points_compare(item["owner"]["display_name"].to_s, val)
        end

        # The key regardless of whether item is track, album,or playlist
        if k == "name"
          pts += points_compare(item["name"].to_s, val)
        end
      end

      points.push([pts, index])
      index += 1
    end

    points.sort!{ |a, b| b[0] <=> a[0] }

    return points
  end

  # Returns an `Int` based off the number of points worth assigning to the 
  # matchiness of the string. First the strings are downcased and then all
  # nonalphanumeric characters are stripped.
  # If the strings are the exact same, return 3 pts.
  # If *item1* includes *item2*, return 1 pt.
  # Else, return 0 pts.
  private def points_compare(item1 : String, item2 : String) : Int32
    item1 = item1.downcase.gsub(/[^a-z0-9]/, "")
    item2 = item2.downcase.gsub(/[^a-z0-9]/, "")

    if item1 == item2
      return 3
    elsif item1.includes?(item2)
      return 1
    else
      return 0
    end
  end

  # Returns a `String` encoded for the spotify api
  #
  # ```
  # query_encode("album", "A Night At The Opera")
  # => "album:A+Night+At+The+Opera"
  # ```
  private def param_encode(key : String, value : String) : String
    return key.gsub(" ", "+") + ":" + value.gsub(" ", "+") + "+"
  end

end


# puts SpotifySearcher.new()
#   .authorize("e4198f6a3f7b48029366f22528b5dc66", 
#              "ba057d0621a5496bbb64edccf758bde5")
#   .find_item("album", {
#     "name" => "A Night At The Opera",
#     "artist" => "Queen"
#   })