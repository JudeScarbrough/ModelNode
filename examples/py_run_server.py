import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import modelnode


# ensure llama3.2 is installed via terminal command "ollama pull llama3.2"
routes = {
    "/llama": "llama3.2"
}


modelnode.run_server(routes, show_prompts=True, show_responses=True)