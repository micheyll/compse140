import http.server
import json
import subprocess
import socket

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def get_processes():
    return subprocess.check_output(['ps', '-e', '-o', 'comm=', '--sort=-%cpu', '|', 'head', '-n', '5'], shell=True).decode().strip().split('\n')

def get_disk_space():
    return subprocess.check_output(['df', '-h', '/', '--output=avail']).decode().split('\n')[1].strip()

def get_uptime():
    return subprocess.check_output(['uptime', '-p']).decode().strip()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            info = {
                "Service2": {
                    "IP address information": get_ip_address(),
                    "List of running processes": get_processes(),
                    "Available disk space": get_disk_space(),
                    "Time since last boot": get_uptime()
                }
            }
            
            self.wfile.write(json.dumps(info, indent=2).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    server_address = ('', 8200)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Service2 listening on port 8200...')
    httpd.serve_forever()
