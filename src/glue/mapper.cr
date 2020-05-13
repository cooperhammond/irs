require "json"

class PlaylistExtensionMapper
  JSON.mapping(
    tracks: {
      type: PlaylistTracksMapper,
      setter: true
    },
    id: String,
    images: JSON::Any,
    name: String,
    owner: JSON::Any,
    type: String
  )
end

class PlaylistTracksMapper
  JSON.mapping(
    items: {
      type: Array(JSON::Any),
      setter: true
    },
    total: Int32
  )
end

class AlbumTracksMapper
  JSON.mapping(
    album: { 
      type: JSON::Any,
      nilable: true,
      setter: true
    },
    artists: JSON::Any,
    disc_number: Int32,
    id: String,
    name: String,
    track_number: Int32,
    type: String,
    uri: String
  )
end


def parse_to_json(string_json : String) : JSON::Any
  return JSON.parse(string_json)
end