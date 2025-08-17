import requests

def get_weather(latitude, longitude):
    """Fetches the current weather for a given latitude and longitude."""
    print(f"--- Calling Weather API for coordinates {latitude}, {longitude} ---")
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve weather data."}

# The description for the AI
weather_tool_description = {
    "name": "get_weather",
    "description": "Get the current weather for a given latitude and longitude.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number", "description": "The latitude of the location."},
            "longitude": {"type": "number", "description": "The longitude of the location."}
        },
        "required": ["latitude", "longitude"]
    }
}