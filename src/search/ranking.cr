alias VID_VALUE_CLASS = String
alias VID_METADATA_CLASS = Hash(String, VID_VALUE_CLASS)
alias YT_METADATA_CLASS = Array(VID_METADATA_CLASS)

module Ranker
  extend self

  GARBAGE_PHRASES = [
    "cover", "album", "live", "clean", "version", "full", "full album", "row",
    "at", "@", "session", "how to", "npr music", "reimagined", "version",
    "trailer"
  ]

  GOLDEN_PHRASES = [
    "official video", "official music video",
  ]

  # Will rank videos according to their title and the user input, returns a sorted array of hashes
  # of the points a song was assigned and its original index
  # *spotify_metadata* is the metadate (from spotify) of the song that you want
  # *yt_metadata* is an array of hashes with metadata scraped from the youtube search result page
  # *query* is the query that you submitted to youtube for the results you now have
  # ```
  # Ranker.rank_videos(spotify_metadata, yt_metadata, query)
  # => [
  #      {"points" => x, "index" => x},
  #      ...
  #    ]
  # ```
  # "index" corresponds to the original index of the song in yt_metadata
  def rank_videos(spotify_metadata : JSON::Any, yt_metadata : YT_METADATA_CLASS,
                  query : String) : Array(Hash(String, Int32))
    points = [] of Hash(String, Int32)
    index = 0

    actual_song_name = spotify_metadata["name"].as_s
    actual_artist_name = spotify_metadata["artists"][0]["name"].as_s

    yt_metadata.each do |vid|
      pts = 0

      pts += points_string_compare(actual_song_name, vid["title"])
      pts += points_string_compare(actual_artist_name, vid["title"])
      pts += count_buzzphrases(query, vid["title"])
      pts += compare_timestamps(spotify_metadata, vid)

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

  # SINGULAR COMPONENT OF RANKING ALGORITHM
  private def compare_timestamps(spotify_metadata : JSON::Any, node : VID_METADATA_CLASS) : Int32
    actual_time = spotify_metadata["duration_ms"].as_i
    vid_time = node["duration_ms"].to_i

    difference = (actual_time - vid_time).abs 

    # puts "actual: #{actual_time}, vid: #{vid_time}"
    # puts "\tdiff: #{difference}"
    # puts "\ttitle: #{node["title"]}"

    if difference <= 1000
      return 3
    elsif difference <= 2000
      return 2
    elsif difference <= 5000
      return 1
    else 
      return 0
    end
  end

  # SINGULAR COMPONENT OF RANKING ALGORITHM
  # Returns an `Int` based off the number of points worth assigning to the
  # matchiness of the string. First the strings are downcased and then all
  # nonalphanumeric characters are stripped.
  # If *item1* includes *item2*, return 3 pts.
  # If after the items have been blanked, *item1* includes *item2*,
  #   return 1 pts.
  # Else, return 0 pts.
  private def points_string_compare(item1 : String, item2 : String) : Int32
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

  # SINGULAR COMPONENT OF RANKING ALGORITHM
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
end