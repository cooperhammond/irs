require "../search/spotify"
require "../search/youtube"

require "../interact/ripper"
require "../interact/tagger"

require "../bottle/styles"

class Song
  @spotify_searcher = SpotifySearcher.new
  @client_id = ""
  @client_secret = ""

  @metadata : JSON::Any?
  getter filename = ""
  @artist = ""
  @album = ""

  @outputs : Hash(String, Array(String)) = {
    "intro" => [Style.bold("[%s by %a]\n")],
    "metadata" => [
      "  Searching for metadata ...\r",
      Style.green("  + ") + Style.dim("Metadata found                  \n")
    ],
    "url" => [
      "  Searching for URL ...\r",
      Style.green("  + ") + Style.dim("URL found                       \n")
    ],
    "download" => [
      "  Downloading video:\n",
      Style.green("\r  + ") + Style.dim("Converted to mp3              \n")
    ],
    "albumart" => [
      "  Downloading album art ...\r",
      Style.green("  + ") + Style.dim("Album art downloaded            \n")
    ],
    "tagging" => [
      "  Attaching metadata ...\r",
      Style.green("  + ") + Style.dim("Metadata attached               \n")
    ],
    "finished" => [
      Style.green("  + ") + "Finished!\n"
    ]
  }

  def initialize(@song_name : String, @artist_name : String)
  end

  # Find, downloads, and tags the mp3 song that this class represents.
  #
  # ```
  # Song.new("Bohemian Rhapsody", "Queen").grab_it
  # ```
  def grab_it
    outputter("intro", 0)

    if !@spotify_searcher.authorized? && !@metadata
      if @client_id != "" && @client_secret != ""
        @spotify_searcher.authorize(@client_id, @client_secret)
      else
        raise("Need to call either `provide_metadata`, `provide_spotify`, " +
              "or `provide_client_keys` so that Spotify can be interfaced with.")
      end
    end

    if !@metadata
      outputter("metadata", 0)
      @metadata = @spotify_searcher.find_item("track", {
        "name"   => @song_name,
        "artist" => @artist_name,
      })

      if !@metadata
        raise("There was no metadata found on Spotify for " +
              %("#{@song_name}" by "#{@artist_name}". ) +
              "Check your input and try again.")
      end
      outputter("metadata", 1)
    end

    data = @metadata.as(JSON::Any)
    @filename = data["track_number"].to_s + " - #{data["name"].to_s}.mp3"

    outputter("url", 0)
    url = Youtube.find_url(@song_name, @artist_name, search_terms: "lyrics")
    if !url
      raise("There was no url found on youtube for " +
            %("#{@song_name}" by "#{@artist_name}. ) +
            "Check your input and try again.")
    end
    outputter("url", 1)

    outputter("download", 0)
    Ripper.download_mp3(url.as(String), @filename)
    outputter("download", 1)

    outputter("albumart", 0)
    temp_albumart_filename = ".tempalbumart.jpg"
    HTTP::Client.get(data["album"]["images"][0]["url"].to_s) do |response|
      File.write(temp_albumart_filename, response.body_io)
    end
    outputter("albumart", 0)

    # check if song's metadata has been modded in playlist, update artist accordingly
    if data["artists"][-1]["owner"]? 
      @artist = data["artists"][-1]["name"].to_s
    else
      @artist = data["artists"][0]["name"].to_s
    end
    @album = data["album"]["name"].to_s

    tagger = Tags.new(@filename)
    tagger.add_album_art(temp_albumart_filename)
    tagger.add_text_tag("title", data["name"].to_s)
    tagger.add_text_tag("artist", @artist)
    tagger.add_text_tag("album", @album)
    tagger.add_text_tag("genre", 
      @spotify_searcher.find_genre(data["artists"][0]["id"].to_s))
    tagger.add_text_tag("track", data["track_number"].to_s)
    tagger.add_text_tag("disc", data["disc_number"].to_s)

    outputter("tagging", 0)
    tagger.save
    File.delete(temp_albumart_filename)
    outputter("tagging", 1)

    outputter("finished", 0)
  end

  # Will organize the song into the user's provided music directory as
  # music_directory > artist_name > album_name > song
  # Must be called AFTER the song has been downloaded.
  #
  # ```
  # s = Song.new("Bohemian Rhapsody", "Queen").grab_it
  # s.organize_it("/home/cooper/Music")
  # # Will move the mp3 file to
  # # /home/cooper/Music/Queen/A Night At The Opera/1 - Bohemian Rhapsody.mp3
  # ```
  def organize_it(music_directory : String)
    path = Path[music_directory].expand(home: true)
    path = path / @artist_name.gsub(/[\/]/, "").gsub("  ", " ")
    path = path / @album.gsub(/[\/]/, "").gsub("  ", " ")
    strpath = path.to_s
    if !File.directory?(strpath)
      FileUtils.mkdir_p(strpath)
    end
    safe_filename = @filename.gsub(/[\/]/, "").gsub("  ", " ")
    File.rename("./" + @filename, (path / safe_filename).to_s)
  end

  # Provide metadata so that it doesn't have to find it. Useful for overwriting
  # metadata. Must be called if provide_client_keys and provide_spotify are not
  # called.
  #
  # ```
  # Song.new(...).provide_metadata(...).grab_it
  # ```
  def provide_metadata(metadata : JSON::Any) : self
    @metadata = metadata
    return self
  end

  # Provide an already authenticated `SpotifySearcher` class. Useful to avoid
  # authenticating over and over again. Must be called if provide_metadata and
  # provide_client_keys are not called.
  #
  # ```
  # Song.new(...).provide_spotify(SpotifySearcher.new
  #   .authenticate("XXXXXXXXXX", "XXXXXXXXXXX")).grab_it
  # ```
  def provide_spotify(spotify : SpotifySearcher) : self
    @spotify_searcher = spotify
    return self
  end

  # Provide spotify client keys. Must be called if provide_metadata and
  # provide_spotify are not called.
  #
  # ```
  # Song.new(...).provide_client_keys("XXXXXXXXXX", "XXXXXXXXX").grab_it
  # ```
  def provide_client_keys(client_id : String, client_secret : String) : self
    @client_id = client_id
    @client_secret = client_secret
    return self
  end

  private def outputter(key : String, index : Int32)
    text = @outputs[key][index]
      .gsub("%s", @song_name)
      .gsub("%a", @artist_name)
    print text
  end
end
