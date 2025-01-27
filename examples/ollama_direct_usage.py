import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import ollama_interaction







model_name = "llama2"  # Replace with the desired model
prompt = "Why is the sky blue?"

# Get the response
response = ollama_interaction.get_response(prompt, model_name)

# Print the response
print(f"Response: {response}")
