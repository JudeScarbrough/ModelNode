import requests
import json

# URL for the GET request
url = "your server url"

# Parameters for the GET request
params = {
    "prompt": "Hello, tell me about the main difference between American and Japanese cars."
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