require 'socket'
require 'net/http'
require 'json'

def get_ip_address
  Socket.ip_address_list.find { |ai| ai.ipv4? && !ai.ipv4_loopback? }&.ip_address || 'Unknown'
end

def get_processes
  `ps -ax`.split("\n")[1..].join("\n")
end

def get_disk_space
  `df -h /`.split("\n")[1]
end

def get_uptime
  `uptime -p`.strip
end

def get_service2_info
  uri = URI('http://service2:8200')
  response = Net::HTTP.get(uri)
  JSON.parse(response)
rescue StandardError => e
  { error: e.message }
end

server = TCPServer.new(8199)
puts "Service1 listening on port 8199..."

loop do
  client = server.accept
  request = client.gets

  if request.start_with? 'GET /'
    service1_info = {
      service1: {
        ip: get_ip_address,
        processes: get_processes,
        disk_space: get_disk_space,
        uptime: get_uptime
      }
    }

    service2_info = get_service2_info

    response = service1_info.merge(service2_info).to_json

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
