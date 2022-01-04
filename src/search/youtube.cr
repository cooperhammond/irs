require "http"
require "xml"
require "json"
require "uri"

require "./ranking"

require "../bottle/config"
require "../bottle/styles"


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
  def find_url(spotify_metadata : JSON::Any,
               flags = {} of String => String) : String?

    search_terms = Config.search_terms

    select_link = flags["select"]?

    song_name = spotify_metadata["name"].as_s
    artist_name = spotify_metadata["artists"][0]["name"].as_s

    human_query = "#{song_name} #{artist_name} #{search_terms.strip}"
    params = HTTP::Params.encode({"search_query" => human_query})

    response = HTTP::Client.get("https://www.youtube.com/results?#{params}")

    yt_metadata = get_yt_search_metadata(response.body)

    if yt_metadata.size == 0
      puts "There were no results for this query on youtube: \"#{human_query}\""
      return nil
    end

    root = "https://youtube.com"
    ranked = Ranker.rank_videos(spotify_metadata, yt_metadata, human_query)

    if select_link
      return root + select_link_menu(spotify_metadata, yt_metadata)
    end

    begin
      puts Style.dim("  Video: ") + yt_metadata[ranked[0]["index"]]["title"]
      return root + yt_metadata[ranked[0]["index"]]["href"]
    rescue IndexError
      return nil
    end

    exit 1
  end

  # Presents a menu with song info for the user to choose which url they want to download
  private def select_link_menu(spotify_metadata : JSON::Any,
                               yt_metadata : YT_METADATA_CLASS) : String
    puts Style.dim("  Spotify info: ") +
         Style.bold("\"" + spotify_metadata["name"].to_s) + "\" by \"" +
         Style.bold(spotify_metadata["artists"][0]["name"].to_s + "\"") +
         " @ " + Style.blue((spotify_metadata["duration_ms"].as_i / 1000).to_i.to_s) + "s"
    puts "  Choose video to download:"
    index = 1
    yt_metadata.each do |vid|
      print "    " + Style.bold(index.to_s + " ")
      puts "\"" + vid["title"] + "\" @ " + Style.blue((vid["duration_ms"].to_i / 1000).to_i.to_s) + "s"
      index += 1
      if index > 5
        break
      end
    end

    input = 0
    while true # not between 1 and 5
      begin
        print Style.bold("  > ")
        input = gets.not_nil!.chomp.to_i
        if input < 6 && input > 0
          break
        end
      rescue
        puts Style.red("  Invalid input, try again.")
      end
    end

    return yt_metadata[input-1]["href"]

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

  # Returns as a valid URL if possible
  #
  # ```
  # Youtube.validate_url("https://www.youtube.com/watch?v=NOTANACTUALVIDEOID")
  # => nil
  # ```
  def validate_url(url : String) : String | Nil
    uri = URI.parse url
    return nil if !uri

    query = uri.query
    return nil if !query

    # find the video ID
    vID = nil
    query.split('&').each do |q|
      if q.starts_with?("v=")
        vID = q[2..-1]
      end
    end
    return nil if !vID

    url = "https://www.youtube.com/watch?v=#{vID}"

    # this is an internal endpoint to validate the video ID
    params = HTTP::Params.encode({"format" => "json", "url" => url})
    response = HTTP::Client.get "https://www.youtube.com/oembed?#{params}"
    return nil unless response.success?

    res_json = JSON.parse(response.body)
    title = res_json["title"].as_s
    puts Style.dim("  Video: ") + title

    return url
  end
end
