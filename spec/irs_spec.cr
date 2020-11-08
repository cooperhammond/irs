require "./spec_helper"

describe CLI do
  # TODO: Write tests

  it "can show help" do
    run_CLI_with_args(["--help"])
  end

  it "can show version" do
    run_CLI_with_args(["--version"])
  end

  # !!TODO: make a long and short version of the test suite
  # TODO: makes so this doesn't need user input
  it "can install ytdl and ffmpeg binaries" do
    # run_CLI_with_args(["--install"])
  end

  it "can show config file loc" do
    run_CLI_with_args(["--config"])
  end

  it "can download a single song" do
    run_CLI_with_args(["--song", "Bohemian Rhapsody", "--artist", "Queen"])
  end

  it "can download an album" do
    run_CLI_with_args(["--artist", "Arctic Monkeys", "--album", "Da Frame 2R / Matador"])
  end

  it "can download a playlist" do
    run_CLI_with_args(["--artist", "prakkillian", "--playlist", "IRS Testing"])
  end
end
