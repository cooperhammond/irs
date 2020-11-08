require "spec"

# https://github.com/mosop/stdio

require "../src/bottle/cli"

def run_CLI_with_args(argv : Array(String))
    cli = CLI.new(argv)
    cli.act_on_args
end