# Uses FFMPEG binary to add metadata to mp3 files
# ```
# t = Tags.new("bohem rap.mp3")
# t.add_album_art("a night at the opera album cover.jpg")
# t.add_text_tag("title", "Bohemian Rhapsody")
# t.save()
# ```
class Tags

  # TODO: export this path to a config file
  @BIN_LOC = Path["~/.irs/bin".sub("~", Path.home)]
  @query_args = [] of String

  # initialize the class with an already created MP3
  def initialize(@filename : String)
    if !File.exists?(@filename)
      raise "MP3 not found at location: #{@filename}"
    end

    @query_args.push(%(-i "#{@filename}"))

  end

  # Add album art to the mp3. Album art must be added BEFORE text tags are.
  # Check the usage above to see a working example.
  def add_album_art(image_location : String) : Nil
    if !File.exists?(image_location)
      raise "Image file not found at location: #{image_location}"
    end

    @query_args.push(%(-i "#{image_location}"))
    @query_args.push("-map 0:0 -map 1:0")
    @query_args.push("-c copy")
    @query_args.push("-id3v2_version 3")
    @query_args.push(%(-metadata:s:v title="Album cover"))
    @query_args.push(%(-metadata:s:v comment="Cover (front)"))
    @query_args.push(%(-metadata:s:v title="Album cover"))
  end

  # Add a text tag to the mp3. If you want to see what text tags are supported,
  # check out: https://wiki.multimedia.cx/index.php?title=FFmpeg_Metadata
  def add_text_tag(key : String, value : String) : Nil
    @query_args.push(%(-metadata #{key}="#{value}"))
  end

  # Run the necessary commands to attach album art to the mp3
  def save : Nil
    @query_args.push(%("_#{@filename}"))
    command = @BIN_LOC.to_s + "/ffmpeg " + @query_args.join(" ")

    l = Logger.new(command, ".tagger.log")
    l.start { |line, start| }
  
    File.delete(@filename)
    File.rename("_" + @filename, @filename)
  end
end

# a = Tags.new("test.mp3")
# a.add_text_tag("title", "Warwick Avenue")
# a.add_album_art("file.png")
# a.save()