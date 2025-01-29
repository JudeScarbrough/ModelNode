import sys
import os


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(parent_dir)


from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import socket
import json
import ollama_interaction
import os

### Documentation available at https://github.com/JudeScarbrough/ModelNode ###

# Define the base directory for static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to handle routes and parameters
def _handle_request(route, params, route_model_map, show_prompts, show_responses):
    if route == "/get-routes":
        # Return the route-to-model mapping as a JSON response
        response = json.dumps(route_model_map, indent=4)
        if show_prompts:
            print(f"Handling route: {route}")
        if show_responses:
            print(f"Response: {response}")
        return response

    # Serve the blank route "/"
    if route == "/":
        filepath = os.path.join(BASE_DIR, "web_ui/index.html")  # Path to the index.html file
        try:
            with open(filepath, "rb") as f:
                response = f.read()  # Read the file content
                if show_prompts:
                    print(f"Handling route: {route}")
                    print(f"Serving: web_ui/index.html")
                return response.decode("utf-8")  # Return the HTML as a string
        except FileNotFoundError:
            error_message = "404 Not Found: index.html not found"
            print(error_message)
            return error_message

    if route in route_model_map:
        model_name = route_model_map[route]  # Get the model name for this route
        if show_prompts:
            print(f"Handling route: {route}")
            print(f"Parameters: {params}")

        if "prompt" in params:
            prompt = params["prompt"][0]  # Extract the prompt parameter
            

            if "context" in params: # only adds context if context exists
                prompt = f"***context for question: { params['context'][0] }***    question to respond to: {params['prompt'][0]}"
            

            try:
                response = ollama_interaction.get_response(prompt, model_name)
                if show_responses:
                    print(f"Response from model '{model_name}': {response}")
                return response
            except Exception as e:
                error_message = f"Error: Model '{model_name}' is not available or could not generate a response. Details: {e}"
                print(error_message)
                return error_message
        else:
            return "Error: Missing 'prompt' parameter"
    
    return f"Error: Route '{route}' not found"

class _RouteHandler(BaseHTTPRequestHandler):
    # This will hold the route-to-model mapping and logging settings
    route_model_map = {}
    show_prompts = False
    show_responses = False

    def _set_cors_headers(self):
        """Set the necessary CORS headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        # Parse the URL and query string
        parsed_path = urlparse.urlparse(self.path)
        route = parsed_path.path  # Extract the route (e.g., "/hello")
        params = urlparse.parse_qs(parsed_path.query)  # Extract query parameters

        # Serve the root route with index.html
        if route == "/":
            filepath = os.path.join(BASE_DIR, "web_ui/index.html")
            try:
                with open(filepath, "rb") as f:
                    self.send_response(200)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found: index.html not found")
                return

        # Serve the styles.css file
        elif route == "/styles.css":
            filepath = os.path.join(BASE_DIR, "web_ui/styles.css")
            try:
                with open(filepath, "rb") as f:
                    self.send_response(200)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "text/css")
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found: web_ui/styles.css not found")
                return

        # Handle other routes
        response_message = _handle_request(
            route,
            params,
            self.route_model_map,
            self.show_prompts,
            self.show_responses
        )

        # Send response
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-type", "application/json" if route == "/get-routes" else "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode("utf-8"))



def _get_private_ip():
    """Get the private IP address of the current machine."""
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        return private_ip
    except socket.error:
        return "Unable to retrieve IP address"

def run_server(route_model_map={"/llama": "llama3.2"}, host="0.0.0.0", port=8000, show_prompts=False, show_responses=False):
    """Run the HTTP server with the given route-to-model mapping, logging settings, and port."""
    private_ip = _get_private_ip()

    # Inject the route-to-model mapping and logging settings into the request handler
    _RouteHandler.route_model_map = route_model_map
    _RouteHandler.show_prompts = show_prompts
    _RouteHandler.show_responses = show_responses



    model_node = r"""
  __  __           _      _ _   _           _      
 |  \/  |         | |    | | \ | |         | |     
 | \  / | ___   __| | ___| |  \| | ___   __| | ___ 
 | |\/| |/ _ \ / _` |/ _ \ | . ` |/ _ \ / _` |/ _ |
 | |  | | (_) | (_| |  __/ | |\  | (_) | (_| |  __/
 |_|  |_|\___/ \__,_|\___|_|_| \_|\___/ \__,_|\___|
"""



    print(model_node)
    print()
    print(f"Starting server on {private_ip}:{port}")
    print()
    print(f"Web user interface accessible at: \033[4;34mhttp://{private_ip}:{port}\033[0m  (ctrl + click (windows) or cmd + click (mac) to open)")
    print()
    print("Routes:")
    for route, model in route_model_map.items():
        print(f"  {route} -> {model}")
    print("  /get-routes -> (Returns the route-to-model mapping)")
    print("  / -> (Serves index.html with styles.css)")
    print()

    server = HTTPServer((host, port), _RouteHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


