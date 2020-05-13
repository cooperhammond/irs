require "colorize"

class Style
  def self.bold(txt)
    txt.colorize.mode(:bold)
  end

  def self.dim(txt)
    txt.colorize.mode(:dim)
  end

  def self.blue(txt)
    txt.colorize(:light_blue)
  end

  def self.green(txt)
    txt.colorize(:light_green)
  end

  def self.red(txt)
    txt.colorize(:light_red)
  end
end
