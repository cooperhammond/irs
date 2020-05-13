require "http"
require "json"
require "base64"

require "../glue/mapper"

class SpotifySearcher
  @root_url = Path["https://api.spotify.com/v1/"]

  @access_header : (HTTP::Headers | Nil) = nil
  @authorized = false

  # Saves an access token for future program use with spotify using client IDs.
  # Specs defined on spotify's developer api:
  # https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
  #
  # ```
  # SpotifySearcher.new.authorize("XXXXXXXXXX", "XXXXXXXXXX")
  # ```
  def authorize(client_id : String, client_secret : String) : self
    auth_url = "https://accounts.spotify.com/api/token"

    headers = HTTP::Headers{
      "Authorization" => "Basic " +
                         Base64.strict_encode "#{client_id}:#{client_secret}",
    }

    payload = "grant_type=client_credentials"

    response = HTTP::Client.post(auth_url, headers: headers, form: payload)
    error_check(response)

    access_token = JSON.parse(response.body)["access_token"]

    @access_header = HTTP::Headers{
      "Authorization" => "Bearer #{access_token}",
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
  def find_item(item_type : String, item_parameters : Hash, offset = 0,
                limit = 20) : JSON::Any?
    query = generate_query(item_type, item_parameters, offset, limit)

    url = @root_url.join("search?q=#{query}").to_s

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)

    items = JSON.parse(response.body)[item_type + "s"]["items"].as_a

    points = rank_items(items, item_parameters)

    to_return = nil

    begin
      # this means no points were assigned so don't return the "best guess"
      if points[0][0] <= 0
        to_return = nil
      else
        to_return = get_item(item_type, items[points[0][1]]["id"].to_s)
      end
    rescue IndexError
      to_return = nil
    end

    # if this triggers, it means that a playlist has failed to be found, so
    # the search will be bootstrapped into find_user_playlist
    if to_return == nil && item_type == "playlist"
      return find_user_playlist(
        item_parameters["username"],
        item_parameters["name"]
      )
    end

    return to_return
  end

  # Grabs a users playlists and searches through it for the specified playlist
  #
  # ```
  # spotify_searcher.find_user_playlist("prakkillian", "the little man")
  # => {playlist metadata}
  # ```
  def find_user_playlist(username : String, name : String, offset = 0,
                         limit = 20) : JSON::Any?
    url = "users/#{username}/playlists?limit=#{limit}&offset=#{offset}"
    url = @root_url.join(url).to_s

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)
    body = JSON.parse(response.body)

    items = body["items"]
    points = [] of Array(Int32)

    items.as_a.each_index do |i|
      points.push([points_compare(items[i]["name"].to_s, name), i])
    end
    points.sort! { |a, b| b[0] <=> a[0] }

    begin
      if points[0][0] < 3
        return find_user_playlist(username, name, offset + limit, limit)
      else
        return get_item("playlist", items[points[0][1]]["id"].to_s)
      end
    rescue IndexError
      return nil
    end
  end

  # Get the complete metadata of an item based off of its id
  #
  # ```
  # SpotifySearcher.new.authorize(...).get_item("artist", "1dfeR4HaWDbWqFHLkxsg1d")
  # ```
  def get_item(item_type : String, id : String, offset = 0,
               limit = 100) : JSON::Any
    if item_type == "playlist"
      return get_playlist(id, offset, limit)
    end

    url = "#{item_type}s/#{id}?limit=#{limit}&offset=#{offset}"
    url = @root_url.join(url).to_s

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)

    body = JSON.parse(response.body)

    return body
  end

  # The only way this method differs from `get_item` is that it makes sure to
  # insert ALL tracks from the playlist into the `JSON::Any`
  #
  # ```
  # SpotifySearcher.new.authorize(...).get_playlist("122Fc9gVuSZoksEjKEx7L0")
  # ```
  def get_playlist(id, offset = 0, limit = 100) : JSON::Any
    url = "playlists/#{id}?limit=#{limit}&offset=#{offset}"
    url = @root_url.join(url).to_s

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)
    body = JSON.parse(response.body)
    parent = PlaylistExtensionMapper.from_json(response.body)

    more_tracks = body["tracks"]["total"].as_i > offset + limit
    if more_tracks
      return playlist_extension(parent, id, offset = offset + limit)
    end

    return body
  end

  # This method exists to loop through spotify API requests and combine all
  # tracks that may not be captured by the limit of 100.
  private def playlist_extension(parent : PlaylistExtensionMapper,
                                 id : String, offset = 0, limit = 100) : JSON::Any
    url = "playlists/#{id}/tracks?limit=#{limit}&offset=#{offset}"
    url = @root_url.join(url).to_s

    response = HTTP::Client.get(url, headers: @access_header)
    error_check(response)
    body = JSON.parse(response.body)
    new_tracks = PlaylistTracksMapper.from_json(response.body)

    new_tracks.items.each do |track|
      parent.tracks.items.push(track)
    end

    more_tracks = body["total"].as_i > offset + limit
    if more_tracks
      return playlist_extension(parent, id, offset = offset + limit)
    end

    return JSON.parse(parent.to_json)
  end

  # Find the genre of an artist based off of their id
  #
  # ```
  # SpotifySearcher.new.authorize(...).find_genre("1dfeR4HaWDbWqFHLkxsg1d")
  # ```
  def find_genre(id : String) : String
    genre = get_item("artist", id)["genres"][0].to_s
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
      # This will map album and track names from the name key to the query
      if k == "name"
        # will remove the "name:<title>" param from the query
        if item_type == "playlist"
          query += item_parameters[k].gsub(" ", "+") + "+"
        else
          query += param_encode(item_type, item_parameters[k])
        end

        # check if the key is to be excluded
      elsif query_exclude.includes?(k)
        next

        # if it's none of the above, treat it normally
        # NOTE: playlist names will be inserted into the query normally, without
        # a parameter.
      else
        query += param_encode(k, item_parameters[k])
      end
    end

    # extra api info
    query += "&type=#{item_type}&limit=#{limit}&offset=#{offset}"

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
          pts_to_add = points_compare(item["owner"]["display_name"].to_s, val)
          pts += pts_to_add
          pts += -10 if pts_to_add == 0
        end

        # The key regardless of whether item is track, album,or playlist
        if k == "name"
          pts += points_compare(item["name"].to_s, val)
        end
      end

      points.push([pts, index])
      index += 1
    end

    points.sort! { |a, b| b[0] <=> a[0] }

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
#   .authorize("XXXXXXXXXXXXXXX",
#              "XXXXXXXXXXXXXXX")
#   .find_item("playlist", {
#     "name" => "Brain Food",
#     "username" => "spotify"
#     # "name " => "A Night At The Opera",
#     # "artist" => "Queen"
#     # "track" => "Bohemian Rhapsody",
#     # "artist" => "Queen"
#   })
