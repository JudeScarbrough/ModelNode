# ModelNode

  

ModelNode is an HTTP server with a user interface designed for interaction with machine learning models. With this package, you can easily map specific HTTP routes to models hosted on your public IP, enabling you to receive prompts and deliver responses from all of your models.

#### Why ModelNode?
ModelNode simplifies the process of integrating machine learning models into your web applications. It provides a cost-free, hassle-free alternative to third-party APIs like OpenAI. By hosting your own server with ModelNode, you can:

- Host multiple custom machine learning models.
- Handle prompts and responses directly for your web app.
- Interact directly with your models using Python.
- Achieve a fully self-sufficient setup without incurring API costs.

If you're building new AI-driven features or scaling existing ones, ModelNode makes backing your web apps with large language models simple and free.
  

## Features

  

- #### Route-to-model mapping  
    Allows mapping of request routes to different models, enabling multiple AI models on a single server.

- #### Support for prompt context  
    Allows context such as code documentation, historical context, or prior conversation history to be included, enabling more accurate and informed responses.  

- #### Web-based UI for sending prompts and viewing responses  
    Provides a simple and intuitive web interface to interact with the server, send queries, and visualize responses.

- #### Example scripts
    Includes ready-to-use scripts demonstrating how to send requests to and run the server

- #### Cross-origin resource sharing (CORS) support  
    Allows access from different domains, making it easier to integrate the service with web applications and external clients.


  


## Package Structure

```
ModelNode/
|   modelnode.py                 # Main server implementation
|   ollama_interaction.py        # Model interaction handler
|   excess_routes.py             # Supports multi-model responses
|   readme.md                    # Package documentation
|   requirements.txt             # Dependencies list
|   __init__.py                  # Package initialization
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



  

## Setup and Installation

  
  
  
  
  
  


  

### Python Prerequisites

  

1.  **Ensure Python 3.8+ is Installed**



- If Python is not installed or the version is older than 3.8, download and install the latest version from [python.org](https://www.python.org/).

  

2.  **Install Required Python Libraries**

- Open a terminal and run the following commands to install the package and necessary libraries:

```bash
git clone https://github.com/JudeScarbrough/ModelNode.git
```
```bash
cd ModelNode
```
```bash
python -m venv --prompt=modelnode .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```

  

### Ollama Prerequisites

  

Ollama is a model-serving tool that allows you to run and serve AI models on your local machine.

  



  

#### Installation Steps for Ollama

  

1. Visit [Ollama's Official Website](https://ollama.com/).

2. Download the installer from the website.

3. Run the downloaded installer and follow the on-screen instructions to complete the installation.

4.  **Download a Model**: After installing Ollama, you can download a model by running the following command in your terminal:

```bash
ollama pull <model_name>
```

- Models can be found [on Ollama's website](https://ollama.com/search).



## Running the Server

  

### Step 1: Define Routes

Define your route-to-model mapping in the `routes` dictionary. Enter your desired routes as keys and model names as values. Ensure you download and correctly type the name of each model you want to support.

  

```python
import ModelNode

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

### Start the Example Server
- Install the llama3.2 model, which the example server requires using the following terminal command
```bash
ollama pull llama3.2
```
- Start the example server
```bash
python examples/py_run_server.py
```

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

### Adding Context to Prompts
To add context to your prompts (knowledge the model may find helpful in responding to your prompt), define it in the parameters sent with your GET request.

```python
import ModelNode

url = "https://localhost:8000"
params = {
    "prompt": "Build a daily schedule for myself.",
    "context" "I typically like to read in the morining."
}

response = requests.get(url, params=params)
print(response.json())
```





### Getting Multiple Model Responses From the Same Prompt

Ensure you define all desired routes when starting the server.

```python
import ModelNode

routes = {
    "/llama3.2": "llama3.2",
    "/deepseek": "deepseek-r1:14b",
    "/llama2": "llama2"
}

ModelNode.run_server(routes)
```

Then, when you make a request to the server ensure you add the route for each desired model starting with a slash and separated by +

```python
import requests
import json

url = "http://172.16.233.226:8000/llama3.2+/llama2+/deepseek"

params = {
    "prompt": "What is the difference between American and European cars?"
}

response = requests.get(url, params=params)

print(response.json())
```

The response shape is structured below

```python
{
    "llama3.2": "llama3.2 sample response",
    "llama2": "llama2 sample response",
    "deepseek-r1:14b": "deepseek-r1:14b sample response"
}
```




### Changing the Server Port

  

To run the server on a different port, specify it in the `run_server` function:

  

```python
ModelNode.run_server(routes, port=8080)
```

  





  

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

