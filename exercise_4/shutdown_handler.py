from http.server import HTTPServer, BaseHTTPRequestHandler
import docker
import time

class ShutdownHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/stop':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Shutting down...')
            
            try:
                client = docker.from_env()
                
                # List of containers to stop first
                containers_to_stop = [
                    'exercise_4_service1_1_1',
                    'exercise_4_service1_2_1',
                    'exercise_4_service1_3_1',
                    'exercise_4_service2_1',
                    'exercise_4_nginx_1'
                ]
                
                # Stop all listed containers
                for name in containers_to_stop:
                    try:
                        container = client.containers.get(name)
                        print(f"Stopping {name}")
                        container.kill()
                    except Exception as e:
                        print(f"Error stopping {name}: {e}")
                
                # Wait 20 seconds
                time.sleep(5)
                
                # Stop ourselves
                container = client.containers.get('exercise_4_shutdown-handler_1')
                container.kill()
                    
            except Exception as e:
                print(f"Error during shutdown: {e}")

if __name__ == '__main__':
    server_address = ('', 8201)
    httpd = HTTPServer(server_address, ShutdownHandler)
    print('Shutdown handler listening on port 8201...')
    httpd.serve_forever()
