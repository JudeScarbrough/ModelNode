import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import modelnode


routes = {
    "/llama": "llama3.2",
    "/deepseek": "deepseek-r1:latest"
}


modelnode.run_server(routes, show_prompts=True, show_responses=True)