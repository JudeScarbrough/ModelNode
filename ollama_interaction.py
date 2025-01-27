import ollama
# requires pip install ollama

def get_response(prompt, model_name):
    """
    Sends a prompt to the specified model and returns the response.

    Args:
        prompt (str): The user input to send to the model.
        model_name (str): The name of the model to use.

    Returns:
        str: The response from the model, or an error message if something goes wrong.
    """
    try:
        # Send the message to the model
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract and return the content of the response
        return response["message"]["content"]
    except Exception as e:
        return f"Error: {e}"



