module Config

  extend self

  def binary_location : String
    path = "~/.irs/bin"
    return Path[path].expand(home: true).to_s
  end
end