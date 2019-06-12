require "http"
require "xml"


module Youtube

  extend self

  VALID_LINK_CLASSES = [
    "yt-simple-endpoint style-scope ytd-video-renderer",
    "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "
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
  def find_url(song_name : String, artist_name : String, search_terms = "", download_first = false)
    query = (song_name + " " + artist_name + " " + search_terms).strip.gsub(" ", "+")

    url = "https://www.youtube.com/results?search_query=" + query 

    response = HTTP::Client.get(url)

    valid_nodes = __get_video_link_nodes(response.body)

    if valid_nodes.size == 0
      puts "There were no results for that query."
      return nil
    end

    root = "https://youtube.com"

    return root + valid_nodes[0]["href"] if download_first

    ranked = __rank_videos(song_name, artist_name, valid_nodes)

    return root + valid_nodes[ranked[0][1]]["href"]
  end

  # Will rank videos according to their title and the user input
  # Returns an `Array` of Arrays each layed out like 
  # [<points>, <original index>].
  private def __rank_videos(song_name, artist_name, nodes : Array(XML::Node))
    points = [] of Array(Int32)
    index = 0

    nodes.each do |node|
      pts = 0

      pts += __points_compare(song_name, node["title"])
      pts += __points_compare(artist_name, node["title"])

      points.push([pts, index])
      index += 1
    end

    points.sort!{ |a, b| b[0] <=> a[0] }

    return points
  end

  # Returns an `Int` based off the number of points worth assigning to the 
  # matchiness of the string. First the strings are downcased and then all
  # nonalphanumeric characters are stripped.
  # If *item1* includes *item2*, return 3 pts.
  # If after the items have been blanked, *item1* includes *item2*, 
  #   return 1 pts.
  # Else, return 0 pts.
  private def __points_compare(item1 : String, item2 : String)
    if item1.includes?(item2)
      return 3
    end

    item1 = item1.downcase.gsub(/[^a-z0-9]/, "")
    item2 = item2.downcase.gsub(/[^a-z0-9]/, "")

    if item1.includes?(item2)
      return 1
    else
      return 0
    end
  end

  # Finds valid video links from a `HTTP::Client.get` request
  # Returns an `Array` of `XML::Node`
  private def __get_video_link_nodes(doc : String)
    nodes = XML.parse(doc).xpath_nodes("//a")
    valid_nodes = [] of XML::Node

    nodes.each do |node|
      if __video_link_node?(node)
        valid_nodes.push(node)
      end
    end

    return valid_nodes
  end

  # Tests if the provided `XML::Node` has a valid link to a video
  # Returns a `Bool`
  private def __video_link_node?(node : XML::Node)
    # If this passes, then the node links to a playlist, not a video
    if node["href"]?
      return false if node["href"].includes?("&list=")
    end

    VALID_LINK_CLASSES.each do |valid_class|
      if node["class"]?
        return true if node["class"].includes?(valid_class)
      end
    end
  end
end