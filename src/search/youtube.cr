require "http"
require "xml"

module Youtube
  extend self

  VALID_LINK_CLASSES = [
    "yt-simple-endpoint style-scope ytd-video-renderer",
    "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link ",
  ]

  GARBAGE_PHRASES = [
    "cover", "album", "live", "clean", "version", "full", "full album", "row",
    "at", "@", "session", "how to", "npr music", "reimagined", "hr version",
    "trailer",
  ]

  GOLDEN_PHRASES = [
    "official video", "official music video",
  ]

  # Finds a youtube url based off of the given information.
  # The query to youtube is constructed like this:
  #   "<song_name> <artist_name> <search terms>"
  # If *download_first* is provided, the first link found will be downloaded.
  #
  # ```
  # Youtube.find_url("Bohemian Rhapsody", "Queen")
  # => "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  # ```
  def find_url(song_name : String, artist_name : String, search_terms = "",
               download_first = false) : String?
    query = (song_name + " " + artist_name + " " + search_terms).strip.gsub(" ", "+")

    url = "https://www.youtube.com/results?search_query=" + query

    response = HTTP::Client.get(url)

    valid_nodes = get_video_link_nodes(response.body)

    if valid_nodes.size == 0
      puts "There were no results for that query."
      return nil
    end

    root = "https://youtube.com"

    return root + valid_nodes[0]["href"] if download_first

    ranked = rank_videos(song_name, artist_name, query, valid_nodes)

    begin
      return root + valid_nodes[ranked[0]["index"]]["href"]
    rescue IndexError
      return nil
    end
  end

  # Will rank videos according to their title and the user input
  # Return:
  # [
  #   {"points" => x, "index" => x},
  #   ...
  # ]
  private def rank_videos(song_name : String, artist_name : String,
                          query : String, nodes : Array(XML::Node)) : Array(Hash(String, Int32))
    points = [] of Hash(String, Int32)
    index = 0

    nodes.each do |node|
      pts = 0

      pts += points_compare(song_name, node["title"])
      pts += points_compare(artist_name, node["title"])
      pts += count_buzzphrases(query, node["title"])

      points.push({
        "points" => pts,
        "index"  => index,
      })
      index += 1
    end

    # Sort first by points and then by original index of the song
    points.sort! { |a, b|
      if b["points"] == a["points"]
        a["index"] <=> b["index"]
      else
        b["points"] <=> a["points"]
      end
    }

    return points
  end

  # Returns an `Int` based off the number of points worth assigning to the
  # matchiness of the string. First the strings are downcased and then all
  # nonalphanumeric characters are stripped.
  # If *item1* includes *item2*, return 3 pts.
  # If after the items have been blanked, *item1* includes *item2*,
  #   return 1 pts.
  # Else, return 0 pts.
  private def points_compare(item1 : String, item2 : String) : Int32
    if item2.includes?(item1)
      return 3
    end

    item1 = item1.downcase.gsub(/[^a-z0-9]/, "")
    item2 = item2.downcase.gsub(/[^a-z0-9]/, "")

    if item2.includes?(item1)
      return 1
    else
      return 0
    end
  end

  # Checks if there are any phrases in the title of the video that would
  # indicate audio having what we want.
  # *video_name* is the title of the video, and *query* is what the user the
  # program searched for. *query* is needed in order to make sure we're not
  # subtracting points from something that's naturally in the title
  private def count_buzzphrases(query : String, video_name : String) : Int32
    good_phrases = 0
    bad_phrases = 0

    GOLDEN_PHRASES.each do |gold_phrase|
      gold_phrase = gold_phrase.downcase.gsub(/[^a-z0-9]/, "")

      if query.downcase.gsub(/[^a-z0-9]/, "").includes?(gold_phrase)
        next
      elsif video_name.downcase.gsub(/[^a-z0-9]/, "").includes?(gold_phrase)
        good_phrases += 1
      end
    end

    GARBAGE_PHRASES.each do |garbage_phrase|
      garbage_phrase = garbage_phrase.downcase.gsub(/[^a-z0-9]/, "")

      if query.downcase.gsub(/[^a-z0-9]/, "").includes?(garbage_phrase)
        next
      elsif video_name.downcase.gsub(/[^a-z0-9]/, "").includes?(garbage_phrase)
        bad_phrases += 1
      end
    end

    return good_phrases - bad_phrases
  end

  # Finds valid video links from a `HTTP::Client.get` request
  # Returns an `Array` of `XML::Node`
  private def get_video_link_nodes(doc : String) : Array(XML::Node)
    nodes = XML.parse(doc).xpath_nodes("//a")
    valid_nodes = [] of XML::Node

    nodes.each do |node|
      if video_link_node?(node)
        valid_nodes.push(node)
      end
    end

    return valid_nodes
  end

  # Tests if the provided `XML::Node` has a valid link to a video
  # Returns a `Bool`
  private def video_link_node?(node : XML::Node) : Bool
    # If this passes, then the node links to a playlist, not a video
    if node["href"]?
      return false if node["href"].includes?("&list=")
    end

    VALID_LINK_CLASSES.each do |valid_class|
      if node["class"]?
        return true if node["class"].includes?(valid_class)
      end
    end
    return false
  end
end
