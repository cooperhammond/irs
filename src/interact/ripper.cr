require "./logger"
require "../bottle/config"

module Ripper
  extend self

  BIN_LOC = Path[Config.binary_location]

  # Downloads the video from the given *video_url* using the youtube-dl binary
  # Will create any directories that don't exist specified in *output_filename*
  #
  # ```
  # Ripper.download_mp3("https://youtube.com/watch?v=0xnciFWAqa0",
  #   "Queen/A Night At The Opera/Bohemian Rhapsody.mp3")
  # ```
  def download_mp3(video_url : String, output_filename : String)
    ydl_loc = BIN_LOC.join("youtube-dl")

    # remove the extension that will be added on by ydl
    output_filename = output_filename.split(".")[..-2].join(".")

    options = {
      "--output" => %("#{output_filename}.%(ext)s"), # auto-add correct ext
      # "--quiet" => "",
      "--verbose"         => "",
      "--ffmpeg-location" => BIN_LOC,
      "--extract-audio"   => "",
      "--audio-format"    => "mp3",
      "--audio-quality"   => "0",
    }

    command = ydl_loc.to_s + " " + video_url
    options.keys.each do |option|
      command += " #{option} #{options[option]}"
    end

    l = Logger.new(command, ".ripper.log")
    o = RipperOutputCensor.new

    return l.start do |line, index|
      o.censor_output(line, index)
    end
  end

  # An internal class that will keep track of what to output to the user or
  # what should be hidden.
  private class RipperOutputCensor
    @dl_status_index = 0

    def censor_output(line : String, index : Int32)
      case line
      when .includes? "[download]"
        if @dl_status_index != 0
          print "\e[1A"
          print "\e[0K\r"
        end
        puts line.sub("[download]", "  ")
        @dl_status_index += 1

        if line.includes? "100%"
          puts "Converting to mp3 ..."
        end
      end
    end
  end
end
