import requests

def get_city_coordinates(city_name):
    """Fetches the latitude and longitude for a given city name."""
    print(f"--- Calling Geocoding API for {city_name} ---")
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(url)
    if response.status_code == 200 and "results" in response.json():
        data = response.json()['results'][0]
        return {"latitude": data['latitude'], "longitude": data['longitude']}
    else:
        return {"error": "Could not find coordinates for the city."}

# The description for the AI
get_city_tool_description = {
    "name": "get_city_coordinates",
    "description": "Get the latitude and longitude for a given city name.",
    "parameters": {
        "type": "OBJECT",
        "properties": {"city_name": {"type": "STRING", "description": "The name of the city."}},
        "required": ["city_name"]
    }
}