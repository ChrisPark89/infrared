import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Custom request handler
class SimpleRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Only handle requests to /api/trigger
        if self.path == '/api/trigger':
            content_length = int(self.headers['Content-Length'])  # Get the size of the data
            post_data = self.rfile.read(content_length)  # Read the data

            try:
                # Parse the JSON data from the POST request
                data = json.loads(post_data)
                print("Received data:", data)  # Print the received data
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "Sensor data received",
                    "status": "success"
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))  # Send the response
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "Invalid JSON format",
                    "status": "failure"
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))  # Send error response
        else:
            # Handle other paths (optional)
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Not found",
                "status": "failure"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

# Set up the HTTP server
def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=5000):
    server_address = ('127.0.0.1', port)  # Listen on all available network interfaces
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()