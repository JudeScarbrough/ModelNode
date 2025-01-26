import server


routes = {
    "/llama": "llama3.2",
    "/deepseek": "deepseek-r1"
}


server.run_server(routes, show_prompts=True, show_responses=True)