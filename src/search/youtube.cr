require "http"
require "xml"
require "json"
require "uri"

require "./ranking"


module Youtube
  extend self

  VALID_LINK_CLASSES = [
    "yt-simple-endpoint style-scope ytd-video-renderer",
    "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link ",
  ]

  # Note that VID_VALUE_CLASS, VID_METADATA_CLASS, and YT_METADATA_CLASS are found in ranking.cr

  # Finds a youtube url based off of the given information.
  # The query to youtube is constructed like this:
  #   "<song_name> <artist_name> <search terms>"
  # If *download_first* is provided, the first link found will be downloaded.
  # If *select_link* is provided, a menu of options will be shown for the user to choose their poison
  #
  # ```
  # Youtube.find_url("Bohemian Rhapsody", "Queen")
  # => "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  # ```
  def find_url(spotify_metadata : JSON::Any, search_terms = "",
               download_first = false, select_link = false) : String?

    song_name = spotify_metadata["name"].as_s
    artist_name = spotify_metadata["artists"][0]["name"].as_s

    human_query = song_name + " " + artist_name + " " + search_terms.strip
    url_query = human_query.gsub(" ", "+")

    url = "https://www.youtube.com/results?search_query=" + url_query

    response = HTTP::Client.get(url)

    yt_metadata = get_yt_search_metadata(response.body)

    if yt_metadata.size == 0
      puts "There were no results for this query on youtube: \"#{human_query}\""
      return nil
    end

    root = "https://youtube.com"

    if download_first
      return root + yt_metadata[0]["href"] 
    end

    if select_link
      # return select_link_menu()
    end

    ranked = Ranker.rank_videos(spotify_metadata, yt_metadata, human_query)

    begin
      return root + yt_metadata[ranked[0]["index"]]["href"]
    rescue IndexError
      return nil
    end

    exit 1
  end
  
  #
  private def select_link_menu() : String

  end

  # Finds valid video links from a `HTTP::Client.get` request 
  # Returns an `Array` of `NODES_CLASS` containing additional metadata from Youtube
  private def get_yt_search_metadata(response_body : String) : YT_METADATA_CLASS
    yt_initial_data : JSON::Any = JSON.parse("{}")

    response_body.each_line do |line|
      # timestamp 11/8/2020:
      # youtube's html page has a line previous to this literally with 'scraper_data_begin' as a comment
      if line.includes?("var ytInitialData")
        # Extract JSON data from line
        data = line.split(" = ")[2].delete(';')
        dataEnd = (data.index("</script>") || 0) - 1

        begin
          yt_initial_data = JSON.parse(data[0..dataEnd])
        rescue
          break
        end
      end
    end

    if yt_initial_data == JSON.parse("{}")
      puts "Youtube has changed the way it organizes its webpage, submit a bug"
      puts "saying it has done so on https://github.com/cooperhammond/irs"
      exit(1)
    end

    # where the vid metadata lives
    yt_initial_data = yt_initial_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

    video_metadata = [] of VID_METADATA_CLASS

    i = 0
    while true
      begin
        # video title
        raw_metadata = yt_initial_data[0]["itemSectionRenderer"]["contents"][i]["videoRenderer"]

        metadata = {} of String => VID_VALUE_CLASS

        metadata["title"] = raw_metadata["title"]["runs"][0]["text"].as_s
        metadata["href"] = raw_metadata["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"].as_s
        timestamp = raw_metadata["lengthText"]["simpleText"].as_s
        metadata["timestamp"] = timestamp
        metadata["duration_ms"] = ((timestamp.split(":")[0].to_i * 60 +
                               timestamp.split(":")[1].to_i) * 1000).to_s


        video_metadata.push(metadata)
      rescue IndexError
        break
      rescue Exception
      end
      i += 1
    end

    return video_metadata
  end

  # Checks if the given URL is a valid youtube URL
  #
  # ```
  # Youtube.is_valid_url("https://www.youtube.com/watch?v=NOTANACTUALVIDEOID")
  # => false
  # ```
  def is_valid_url(url : String) : Bool
    uri = URI.parse url

    # is it a video on youtube, with a query
    query = uri.query
    if uri.host != "www.youtube.com" || uri.path != "/watch" || !query
      return false
    end


    queries = query.split('&')

    # find the video ID
    i = 0
    while i < queries.size
      if queries[i].starts_with?("v=")
        vID = queries[i][2..-1]
        break
      end
      i += 1
    end

    if !vID
      return false
    end


    # this is an internal endpoint to validate the video ID
    response = HTTP::Client.get "https://www.youtube.com/get_video_info?video_id=#{vID}"

    return response.body.includes?("status=ok")
  end
end