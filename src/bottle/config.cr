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
    return "362f75b91aeb471bb392945f93eba842"
  end

  def client_secret : String
    return "013556dd71e14e1da9443dee73e23a91"
  end
end