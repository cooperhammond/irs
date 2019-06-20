# TODO: write comments/documentation

class Tags

  @BIN_LOC = Path["~/.irs/bin".sub("~", Path.home)]
  @query_args = [] of String


  def initialize(@filename : String)
    if !File.exists?(@filename)
      raise "MP3 not found at location: #{@filename}"
    end

    @query_args.push(%(-i "#{@filename}"))

  end

  def add_text_tag(key : String, value : String) : Nil
    @query_args.push(%(-metadata #{key}="#{value}"))
  end

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

  def save : Nil
    @query_args.push(%("_#{@filename}"))
    command = @BIN_LOC.to_s + "/ffmpeg " + @query_args.join(" ")
    system(command)

    File.delete(@filename)
    File.rename("_" + @filename, @filename)
  end
end

# a = Tags.new("test.mp3")
# a.add_text_tag("title", "Warwick Avenue")
# a.add_album_art("file.png")
# a.save()