module Pattern
  extend self

  def parse(formatString : String, metadata : JSON::Any)
    formatted : String = formatString

    date : Array(String) = (metadata["album"]? || JSON.parse("{}"))["release_date"]?.to_s.split('-')

    keys : Hash(String, String) = {
      "artist" => ((metadata.dig?("artists") || JSON.parse("{}"))[0]? || JSON.parse("{}"))["name"]?.to_s,
      "title" => metadata["name"]?.to_s,
      "album" => (metadata["album"]? || JSON.parse("{}"))["name"]?.to_s,
      "track_number" => metadata["track_number"]?.to_s,
      "disc_number" => metadata["disc_number"]?.to_s,
      "total_tracks" => (metadata["album"]? || JSON.parse("{}"))["total_tracks"]?.to_s,
      "year" => date[0]?.to_s,
      "month" => date[1]?.to_s,
      "day" => date[2]?.to_s,
      "id" => metadata["id"]?.to_s
    }

    keys.each do |pair|
      formatted = formatted.gsub("{#{pair[0]}}", pair[1] || "")
    end

    return formatted
  end
end
