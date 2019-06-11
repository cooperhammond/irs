require "base64"

require "spotify"


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
  def authorize(client_id : String, client_secret : String)
    auth_url = "https://accounts.spotify.com/api/token"

    headers = HTTP::Headers{
      "Authorization" => "Basic " + 
        Base64.strict_encode "#{client_id}:#{client_secret}"
    }

    payload = "grant_type=client_credentials"

    response = HTTP::Client.post(auth_url, headers: headers, form: payload)

    if response.status_code == 200
      access_token = JSON.parse(response.body)["access_token"]
      
      @access_header = HTTP::Headers{
        "Authorization" => "Bearer #{access_token}"
      }

      @authorized = true

    end

    return self
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
  def find_item(item_type : String, item_parameters : Hash, offset=0, limit=20)

    query = __generate_query(item_type, item_parameters, offset, limit)

    url = @root_url.join("search?q=#{query}").to_s()

    response = HTTP::Client.get(url, headers: @access_header)

    if response.status_code != 200
      puts "There was an error with your request."
      puts "Status code: #{response.status_code}"
      puts "Reponse: \n#{response.body}"
      return nil
    end

    items = JSON.parse(response.body)[item_type + "s"]["items"].as_a

    points = __rank_items(items, item_parameters)

    return items[points[0][1]]

  end
  
  # Generates url to run a GET request against
  private def __generate_query(item_type : String, item_parameters : Hash,
  offset : Int32, limit : Int32)
    query = ""

    # parameter keys to exclude in the api request. These values will be put
    # in, just not their keys.
    query_exclude = ["username"]

    item_parameters.keys.each do |k|
      # This will map album, playlist, and track from the name key to the query
      if k == "name"
        query += __param_encode(item_type, item_parameters[k])

      # check if the key is to be excluded
      elsif !query_exclude.includes?(k)
        query += item_parameters[k].gsub(" ", "+") + "+"

      # if it's none of the above, treat it normally
      else
        query += __param_encode(k, item_parameters[k])
      end
    end

    # extra api info
    query += "&type=#{item_type}&offset=#{offset}&limit=#{limit}"

    return query
  end

  # Ranks the given items based off of the info from parameters.
  # Meant to find the item that the user desires.
  private def __rank_items(items : Array, parameters : Hash)
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
          pts += __points_compare(item["artists"][0]["name"].to_s, val)
        end

        # The key to compare to for playlists
        if k == "username"
          pts += __points_compare(item["owner"]["display_name"].to_s, val)
        end

        # The key regardless of whether item is track, album,or playlist
        if k == "name"
          pts += __points_compare(item["name"].to_s, val)
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
  private def __points_compare(item1 : String, item2 : String)
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

  # Returns a parameter encoded for the spotify api
  #
  # ```
  # __query_encode("album", "A Night At The Opera")
  # => "album:A+Night+At+The+Opera"
  # ```
  private def __param_encode(key : String, value : String)
    return key.gsub(" ", "+") + ":" + value.gsub(" ", "+") + "+"
  end

end


puts SpotifySearcher.new()
  .authorize("e4198f6a3f7b48029366f22528b5dc66", 
             "ba057d0621a5496bbb64edccf758bde5")
  .find_item("track", {
    "name" => "Bohemian Rhapsody",
    "artist" => "Queen"
  })