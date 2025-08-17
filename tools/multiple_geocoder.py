import requests

def get_city_coordinates(city_name):
    """
    Fetches a list of possible coordinates for a given city name.
    Returns a list of dictionaries, each with city details.
    """
    print(f"--- Calling Geocoding API for {city_name} ---")
    
    # 1. Ask for up to 5 results
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=5"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # 2. Use .get() for safety and return the whole list
        results = data.get("results") 
        if results:
            return results
        
    return {"error": "Could not find coordinates for the city."}

# The description for the AI (no changes needed here)
geocoder_tool_description = {
    "name": "get_city_coordinates",
    "description": "Get a list of possible locations and their coordinates for a given city name.",
    "parameters": {
        "type": "object",
        "properties": {"city_name": {"type": "string", "description": "The name of the city."}},
        "required": ["city_name"]
    }
}