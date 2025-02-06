import sys
import os
import json
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(parent_dir)
import ollama_interaction





def handle(route, route_model_map, params):

    if "prompt" in params:


        words = route.split('+')  # Split the route by '+'
        
        all_in_map = all(word in route_model_map for word in words)  # Check if all words are in route_model_map

        if all_in_map:

            response = {}

            for model_route in words:
                model_response = ollama_interaction.get_response(params["prompt"][0], route_model_map[model_route])

                response[route_model_map[model_route]] = model_response

            
            print(params["prompt"][0])
            return json.dumps(response)


        else:
            return "Error: requested models not currently supported in route map"

    return "Error: no prompt in parameters"