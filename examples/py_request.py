import requests
import json

# Ensure you set your proper URL
url = "https:/localhost:8000/llama"

# Parameters for the GET request
params = {
    "prompt": "What is the difference between American and European cars?",
    #"context": "context for you question" <-- add context here if desired
}


try:
    # Sending the GET request
    response = requests.get(url, params=params)
    
    # Checking the response status code
    if response.status_code == 200:
        # Check if the response is JSON
        try:
            data = response.json()
            print("Response data (JSON):", data)
        except ValueError:
            print("Response is not JSON. Raw content:")
            print(response.text)
    else:
        print(f"Error: Received status code {response.status_code}")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)