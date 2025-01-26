from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import socket
import json
import analyze

# Function to handle routes and parameters
def handle_request(route, params, route_model_map, show_prompts, show_responses):
    if route == "/get-routes":
        # Return the route-to-model mapping as a JSON response
        response = json.dumps(route_model_map, indent=4)
        if show_prompts:
            print(f"Handling route: {route}")
        if show_responses:
            print(f"Response: {response}")
        return response

    if route in route_model_map:
        model_name = route_model_map[route]  # Get the model name for this route
        if show_prompts:
            print(f"Handling route: {route}")
            print(f"Parameters: {params}")

        if "prompt" in params:
            prompt = params["prompt"][0]  # Extract the prompt parameter

            try:
                response = analyze.get_response(prompt, model_name)
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

class RouteHandler(BaseHTTPRequestHandler):
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

        # Call the function with the route, parameters, and model map
        response_message = handle_request(
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


def get_private_ip():
    """Get the private IP address of the current machine."""
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        return private_ip
    except socket.error:
        return "Unable to retrieve IP address"

def run_server(route_model_map, host="0.0.0.0", port=8000, show_prompts=False, show_responses=False):
    """Run the HTTP server with the given route-to-model mapping, logging settings, and port."""
    private_ip = get_private_ip()

    # Inject the route-to-model mapping and logging settings into the request handler
    RouteHandler.route_model_map = route_model_map
    RouteHandler.show_prompts = show_prompts
    RouteHandler.show_responses = show_responses

    print(f"Starting server on {host}:{port}...")
    print(f"Accessible on your local network at: http://{private_ip}:{port}")
    print("Routes:")
    for route, model in route_model_map.items():
        print(f"  {route} -> {model}")
    print("  /get-routes -> (Returns the route-to-model mapping)")

    server = HTTPServer((host, port), RouteHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    # Example route-to-model mapping
    routes = {
        "/hello": "llama3.2",
        "/goodbye": "llama2"
    }

    # You can specify the port here, or leave it to default to 8000
    custom_port = 8080  # Change this to any port you like, or remove it to use the default
    run_server(routes, port=custom_port, show_prompts=True, show_responses=True)
