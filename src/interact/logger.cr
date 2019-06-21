class Logger

  @done_signal = "---DONE---"

  @command : String

  def initialize(command : String, @log_name : String, @sleept = 0.01)
    # Have the command output its information to a log and after the command is
    # finished, append an end signal to the document
    @command = "#{command} > #{@log_name} " # standard output to log
    @command += "2> #{@log_name} && " # errors to log
    @command += "echo #{@done_signal} >> #{@log_name}" # 
  end

  # Run @command in the background and pipe its output to the log file, with
  # something constantly monitoring the log file and yielding each new line to
  # the block call. Useful for changing the output of binaries you don't have 
  # much control over.
  # Note that the created temp log will be deleted unless the command fails 
  # its exit or .start is called with delete_file: false
  #
  # ```
  # l = Logger.new(".temp.log", %(echo "CIA spying" && sleep 2 && echo "new veggie tales season"))
  # l.start do |output, index|
  #   case output
  #   when "CIA spying"
  #     puts "i sleep"
  #   when .includes?("veggie tales")
  #     puts "real shit"
  #   end
  # end
  # ```
  def start(delete_file=true, &block) : Bool
    # Delete the log if it already exists
    File.delete(@log_name) if File.exists?(@log_name)

    # Run the command in the background
    called = future {
      system(@command)
    }

    # Wait for the log file to be written to
    while !File.exists?(@log_name) 
      sleep @sleept
    end

    log = File.open(@log_name)
    log_content = read_file(log)
    index = 0

    while true
      temp_content = read_file(log)

      # make sure that there is new data
      if temp_content.size > 0 && log_content != temp_content
        log_content = temp_content

        # break the loop if the command has completed
        break if log_content[0] == @done_signal

        # give the line and index to the block
        yield log_content[0], index
        index += 1
      end
    end

    status = called.get()
    if status == true && delete_file == true 
      log.delete()
    end

    return called.get()
  end

  # Reads each line of the file into an Array of Strings
  private def read_file(file : IO) : Array(String)
    content = [] of String

    file.each_line do |line|
      content.push(line)
    end

    return content
  end
end