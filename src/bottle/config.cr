module Config

  extend self

  def binary_location : String
    path = "~/.irs/bin"
    return Path[path].expand(home: true).to_s
  end

  def music_directory : String
    path = "./Music/"
    return Path[path].expand(home: true).to_s
  end

  def client_key : String
    return "e4198f6a3f7b48029366f22528b5dc66"
  end

  def client_secret : String
    return "ba057d0621a5496bbb64edccf758bde5"
  end
end