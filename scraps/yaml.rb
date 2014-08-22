require 'optparse'
require 'yaml'
# wow my first ruby test file: 2014-03-10

options = {}
#options[:config] = "config/config.yaml"
#options[:config] = "test.yaml"
options[:config] = "../test.yaml"
  
opt_parser = OptionParser.new do |opts|
  opts.banner = "Usage: opttest.rb [options]"

  opts.separator ""
  opts.separator "Options:"
      
  opts.on("-c", "--config [CONFIG]",
          "Specify the file to use as config") do |conf|
    options[:config] = conf
  end
end

opt_parser.parse!
  
#puts options[:config]
begin
  $config = YAML.load_file(options[:config])
  puts "Information on " + options[:config] + ":"
  puts "Customer name: " << $config["customer"]["name"] << " " << $config["customer"]["surname"]
  puts "Date issued: " + $config["date"].to_s
  puts "Bill to: ".concat($config["address"]).concat(", ").concat($config["city"])
  puts "Details: " << $config["details"]
rescue
  puts "An error occurred while reading the specified file!"
end
