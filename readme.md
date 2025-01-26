# ModelNode

ModelNode is a lightweight HTTP server and client interface for interacting with machine learning models via RESTful APIs. This project allows you to map specific routes to machine learning models, handle requests, and serve a web-based user interface for interacting with the models.

## Features

- Route-to-model mapping
- CORS support
- Logging for requests and responses
- Web-based UI for sending prompts and viewing responses
- Example scripts for model interaction and testing

---

## Project Structure

```
ModelNode/
|-- modelnode.py                 # Main server implementation
|-- ollama_interaction.py        # Model interaction handler
|-- client_example.py            # Example client script for testing
|-- server_example.py            # Example script to run the server
|-- web_ui/
    |-- index.html               # Frontend interface
    |-- styles.css               # Frontend styling
```

---

## Setup and Installation

### Prerequisites

1. Python 3.8+
2. Install required dependencies:

```bash
pip install requests
```

3. (Optional) Install additional dependencies for your models.

---

## Running the Server

### Step 1: Define Routes
Define your route-to-model mapping in the `routes` dictionary. Example:

```python
routes = {
    "/llama": "llama3.2",
    "/deepseek": "deepseek-r1:latest"
}
```

### Step 2: Run the Server

Use the `run_server` function to start the HTTP server:

```bash
python server_example.py
```

By default, the server runs on `http://0.0.0.0:8000` and serves the following endpoints:

- `/` - Serves the web UI (`index.html`)
- `/get-routes` - Returns the route-to-model mapping
- Custom routes (e.g., `/llama`) - Interact with specific models

---

## Example Usage

### Sending Requests to the Server

Use the provided example client script to send GET requests:

```python
import requests

url = "http://localhost:8000/llama"
params = {"prompt": "What is the capital of France?"}
response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

### Interacting via the Web UI

1. Open `http://localhost:8000` in your browser.
2. Select a model from the dropdown menu.
3. Enter your prompt and submit.

---

## Customization

### Adding New Routes

To add new routes, modify the `routes` dictionary in the server script:

```python
routes = {
    "/new-model": "new-model-version"
}
```

### Changing the Server Port

To run the server on a different port, specify it in the `run_server` function:

```python
run_server(routes, port=8080)
```

---

## Advanced Features

### Logging Requests and Responses

Enable logging of requests and responses by setting the following parameters to `True` in `run_server`:

```python
run_server(routes, show_prompts=True, show_responses=True)
```

### Static File Hosting

The server serves static files like `index.html` and `styles.css` from the `web_ui/` directory. Ensure that these files are present in the specified path.

---

## Example Scripts

### `ollama_interaction.py`

Handles interaction with models. Example:

```python
from ollama_interaction import get_response

model_name = "llama3.2"
prompt = "Why is the sky blue?"
response = get_response(prompt, model_name)
print(response)
```

### `client_example.py`

A sample client script for testing the server:

```python
import requests
url = "http://localhost:8000/llama"
params = {"prompt": "Tell me a joke."}
response = requests.get(url, params=params)
print(response.json())
```

---

## Contributing

Feel free to open issues or submit pull requests for enhancements and bug fixes. Contributions are welcome!

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

