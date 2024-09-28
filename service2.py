import socket
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_processes():
    return subprocess.check_output(['ps', '-ax']).decode('utf-8')

def get_disk_space():
    return subprocess.check_output(['df', '-h', '/']).decode('utf-8').split('\n')[1]

def get_uptime():
    return subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()

class Service2Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            info = {
                'service2': {
                    'ip': get_ip_address(),
                    'processes': get_processes(),
                    'disk_space': get_disk_space(),
                    'uptime': get_uptime()
                }
            }
            
            self.wfile.write(json.dumps(info).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    server_address = ('', 8200)
    httpd = HTTPServer(server_address, Service2Handler)
    print('Service2 listening on port 8200...')
    httpd.serve_forever()
