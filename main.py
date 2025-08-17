import os
import google.generativeai as genai
from tools.geocoder import get_city_coordinates, get_city_tool_description
from tools.geoweather import get_weather, get_weather_tool_description
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

tools = [get_city_tool_description, get_weather_tool_description]

# Initialize the model with the tools
model = genai.GenerativeModel('gemini-2.5-flash-lite', tools=tools)
chat = model.start_chat()

print("Weather Assistant is ready! Ask me for the weather. Type 'quit' to exit.")

while True:
    user_query = input("> ")
    if user_query.lower() == 'quit':
        break

    # Send the user query to the model
    response = chat.send_message(user_query)
    
    while True:
        # Check if the model wants to call a function
        try:
            function_call = response.candidates[0].content.parts[0].function_call
        except (IndexError, AttributeError):
            # If there's no function call, just print the text response
            print(response.text)
            break

        # If the model *does* want to call a function...
        tool_name = function_call.name
        if function_call.args:
            tool_args = {key: value for key, value in function_call.args.items()}
        else:
            break

        print(f"AI wants to call tool: {tool_name} with arguments: {tool_args}")
        
        # Call the correct Python function based on the tool name
        if tool_name == "get_city_coordinates":
            function_response = get_city_coordinates(**tool_args)
        elif tool_name == "get_weather":
            function_response = get_weather(**tool_args)
        else:
            function_response = {"error": "Unknown tool called by the model."}

        # Send the function's result back to the AI
        response = chat.send_message(
            [{"function_response": {"name": tool_name, "response": function_response}}]
        )

        # Print the AI's final, natural language response
        print(response.candidates[0].content.parts[0].text)