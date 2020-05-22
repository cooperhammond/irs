require "colorize"

class Style
  def self.bold(txt)
    txt.colorize.mode(:bold).to_s
  end

  def self.dim(txt)
    txt.colorize.mode(:dim).to_s
  end

  def self.blue(txt)
    txt.colorize(:light_blue).to_s
  end

  def self.green(txt)
    txt.colorize(:light_green).to_s
  end

  def self.red(txt)
    txt.colorize(:light_red).to_s
  end
end
