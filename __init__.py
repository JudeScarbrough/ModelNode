# ModelNode/__init__.py
from .modelnode import run_server  # Import all functions/classes from modelnode.py
from .ollama_interaction import get_response  # Import all functions/classes from ollama_interaction.py

__all__ = [run_server, get_response]