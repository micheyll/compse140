require 'socket'
require 'net/http'
require 'json'

def get_ip_address
  Socket.ip_address_list.find { |ai| ai.ipv4? && !ai.ipv4_loopback? }&.ip_address || 'Unknown'
end

def get_processes
  `ps -e -o comm= | head -n 5`.split("\n").map(&:strip)
end

def get_disk_space
  `df -h / | tail -n 1 | awk '{print $4}'`.strip
end

def get_uptime
  `uptime -p`.strip
end

def get_service2_info
  uri = URI('http://service2:8200')
  response = Net::HTTP.get(uri)
  JSON.parse(response)
rescue StandardError => e
  { "error" => e.message }
end

server = TCPServer.new(8199)
puts "Service1 listening on port 8199..."

loop do
  client = server.accept
  request = client.gets

  if request.start_with? 'GET /'
    service1_info = {
      "Service1" => {
        "IP address information" => get_ip_address,
        "List of running processes" => get_processes,
        "Available disk space" => get_disk_space,
        "Time since last boot" => get_uptime
      }
    }

    service2_info = get_service2_info

    response = JSON.pretty_generate(service1_info.merge(service2_info))

    client.puts "HTTP/1.1 200 OK"
    client.puts "Content-Type: application/json"
    client.puts "Content-Length: #{response.bytesize}"
    client.puts
    client.puts response
  else
    client.puts "HTTP/1.1 404 Not Found"
  end

  client.close
end
