module Ripper

  extend self

  BIN_LOC = Path["~/.irs/bin".sub("~", Path.home)]

  # Downloads the video from the given *video_url* using the youtube-dl binary
  # Will create any directories that don't exist specified in *output_filename*
  #
  # ```
  # Ripper.download_mp3("https://youtube.com/watch?v=0xnciFWAqa0", 
  #   "Queen/A Night At The Opera/Bohemian Rhapsody.mp3")
  # ```
  def download_mp3(video_url : String, output_filename : String) : Bool
    ydl_loc = BIN_LOC.join("youtube-dl")
    
    # remove the extension that will be added on by ydl
    output_filename = output_filename.split(".")[..-2].join(".")

    # TODO: update the logger for this. Explore overwriting stdout and 
    # injecting/removing text
    options = {
      "--output" => %("#{output_filename}.%(ext)s"), # auto-add correct ext
      # "--quiet" => "",
      "--ffmpeg-location" => BIN_LOC,
      "--extract-audio" => "",
      "--audio-format" => "mp3",
      "--audio-quality" => "0",
    }

    command = ydl_loc.to_s + " " + video_url
    options.keys.each do |option|
      command += " #{option} #{options[option]}"
    end

    if system(command)
      return true
    else
      return false
    end
  end

end