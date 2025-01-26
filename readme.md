# ModelNode

  

ModelNode is a lightweight and efficient HTTP server and client interface designed for seamless interaction with machine learning models. With this package, you can easily map specific HTTP routes to models hosted on your public IP, enabling you to receive prompts and deliver responses from your models in real-time.

#### Why ModelNode?
ModelNode simplifies the process of integrating machine learning models into your web applications. It provides a cost-free, hassle-free alternative to third-party APIs like OpenAI. By hosting your own server with ModelNode, you can:

- Host custom machine learning models.
- Handle prompts and responses directly from your web app.
- Achieve a fully self-sufficient setup without incurring API costs.
If you're building innovative AI-driven features or scaling existing ones, ModelNode makes backing your web apps with large language models fast, simple, and free.
  

## Features

  

- Route-to-model mapping

- Logging for requests and responses

- Web-based UI for sending prompts and viewing responses

- Example scripts for model interaction and testing

 - Cross origin resource sharing support

  


## Package Structure

```
ModelNode/
|   modelnode.py                 # Main server implementation
|   ollama_interaction.py        # Model interaction handler
|   readme.md                    # Package documentation
|
+---examples
|       ollama_direct_usage.py   # Example script for direct model usage
|       py_request.py            # Example script for testing client requests
|       py_run_server.py         # Example script for running the server
|
+---web_ui
|       index.html               # Frontend interface
|       styles.css               # Frontend styling
```

---

  

## Setup and Installation

  
  
  
  
  
  


  

### Python Prerequisits

  

1.  **Ensure Python 3.8+ is Installed**



- If Python is not installed or the version is older than 3.8, download and install the latest version from [python.org](https://www.python.org/).

  

2.  **Install Required Python Libraries**

- Open a terminal or command prompt and run the following command to install the necessary libraries:

  

```bash

pip install requests ollama

```

  

### Ollama Prerequisits

  

Ollama is a model serving tool that allows you to run and serve AI models on your local machine.

  



  

#### Installation Steps for Ollama

  

1. Visit [Ollama's Official Website](https://ollama.com/).

2. Download the installer from the website.

3. Run the downloaded installer and follow the on-screen instructions to complete the installation.

4.  **Download a Model**: After installing Ollama, you can download a model by running the following command in your terminal or command prompt:

```bash

ollama pull <model_name>

```

- Models can be found [on Ollama's website](https://ollama.com/search).

  

## Running the Server

  

### Step 1: Define Routes

Define your route-to-model mapping in the `routes` dictionary. Enter your desired routes as keys and model names as values.

  

```python
routes = {
	"/llama": "llama3.2",
	"/deepseek": "deepseek-r1:latest"
}
```

  

### Step 2: Run the Server

  

Use the `run_server` function to start the HTTP server:

  

```python
import ModelNode

routes = {
	"/llama": "llama3.2",
	"/deepseek": "deepseek-r1:latest"
}

ModelNode.run_server(routes)
```

  

By default, the server runs on `http://0.0.0.0:8000` and serves the following endpoints:

  

-  `/` - Serves the web UI (`index.html`)

-  `/get-routes` - Returns the route-to-model mapping

- Specified route map (e.g., `/llama`) - to Interact with specific models

  


  

## Example Usage

  

### Sending Requests to the Server

  

Use the provided example client script to send GET requests:

  

```python
import requests

url = "http://localhost:8000/llama"
params = {"prompt": "What is the capital of France?"}

response = requests.get(url, params=params)

print(response.json())
```

  

### Interacting via the Web UI

  

1. Open `http://localhost:8000` in your browser.

2. Select a model from the dropdown menu.

3. Enter your prompt and submit.

  



  

## Customization

  

### Adding New Routes

  

To add new routes, modify the `routes` dictionary in the server script:

  

```python
routes = {
	"/new-model": "new-model-name"
}
```

  

### Changing the Server Port

  

To run the server on a different port, specify it in the `run_server` function:

  

```python
ModelNode.run_server(routes, port=8080)
```

  



  

## Advanced Features

  

### Logging Requests and Responses

  

Enable logging of requests and responses by setting the following parameters to `True` in `run_server`:

  

```python
ModelNode.run_server(routes, show_prompts=True, show_responses=True)
```


  

### Interact with Ollama Directly without the Server

  

Handles interaction with models. Example:

  

```python
import ModelNode

model_name = "llama3.2"
prompt = "Why is the sky blue?"

response = ModelNode.get_response(prompt, model_name)

print(response)
```

 
  

## Contributing

Feel free to open issues or submit pull requests for enhancements and bug fixes. Contributions are welcome!

