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
                
                # Base names for the containers
                base_names = [
                    'service1_1',
                    'service1_2',
                    'service1_3',
                    'service2',
                    'nginx'
                ]
                
                # Try both naming conventions for each container
                for base in base_names:
                    hyphen_name = f'exercise_4-{base}-1'
                    underscore_name = f'exercise_4_{base}_1'
                    
                    try:
                        container = client.containers.get(hyphen_name)
                        print(f"Stopping {hyphen_name}")
                        container.stop()
                    except:
                        try:
                            container = client.containers.get(underscore_name)
                            print(f"Stopping {underscore_name}")
                            container.stop()
                        except:
                            print(f"Could not find container with either {hyphen_name} or {underscore_name}")
                
                # Wait 20 seconds
                time.sleep(20)
                
                # Try to stop ourselves with either naming convention
                try:
                    container = client.containers.get('exercise_4-shutdown-handler-1')
                    container.stop()
                except:
                    try:
                        container = client.containers.get('exercise_4_shutdown-handler_1')
                        container.stop()
                    except Exception as e:
                        print(f"Error stopping shutdown handler: {e}")
                    
            except Exception as e:
                print(f"Error during shutdown: {e}")

if __name__ == '__main__':
    server_address = ('', 8201)
    httpd = HTTPServer(server_address, ShutdownHandler)
    print('Shutdown handler listening on port 8201...')
    httpd.serve_forever()
