require "./bottle/cli"

def main
  cli = CLI.new(ARGV)
  cli.act_on_args
end

main()
