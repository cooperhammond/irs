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

  # Searches spotify and returns track metadata in `Hash` format.
  #
  # ```
  # spotify_searcher.find_track("Bohemian Rhapsody", "Queen")
  # => hash of metadata
  # ```
  def find_track(track_name : String, artist_name : String)
    
    query = "track:#{track_name.sub(" ", "+")}+" +
            "artist:#{artist_name.sub(" ", "+")}" + 
            "&type=track"

    url = @root_url.join("search?q=#{query}").to_s()

    response = HTTP::Client.get(url, headers: @access_header)

    puts response.body

  end

  # Searches spotify with the specified parameters for the specified items
  #
  # ```
  # spotify_searcher.find_item("track", {
  #   "artist" => "Queen",
  #   "track" => "Bohemian Rhapsody"
  # })
  # ```
  def find_item(item_type : String, item_parameters : Hash)
    query = ""

    item_parameters.keys.each do |i|
      query += "#{i.sub(" ", "+")}:#{item_parameters[i].sub(" ", "+")}+"
    end
    query += "&type=#{item_type}"

    url = @root_url.join("search?q=#{query}").to_s()

    response = HTTP::Client.get(url, headers: @access_header)

    if response.status_code != 200
      puts "There was an error with your request."
      puts "Status code #{response.status_code}"
      return nil
    end

    items = JSON.parse(response.body)[item_type + "s"]

  end

end


SpotifySearcher.new
  .authorize("e4198f6a3f7b48029366f22528b5dc66", 
             "ba057d0621a5496bbb64edccf758bde5")
  .find_item("track", {
    "artist" => "Queen",
    "track" => "Bohemian Rhapsody"
  })