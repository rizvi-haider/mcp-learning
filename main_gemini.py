import os
from dotenv import load_dotenv
import google.generativeai as genai

# Correctly import both the functions and their descriptions
from tools.geocoder import get_city_coordinates, get_city_tool_description
from tools.geoweather import get_weather, get_weather_tool_description


def main():
    # --- Load API Key ---
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please create a .env file.")
        return
    genai.configure(api_key=api_key)

    # --- Setup the Model with the descriptions ---
    tools = [get_city_tool_description, get_weather_tool_description]
    model = genai.GenerativeModel('gemini-2.5-flash-lite', tools=tools)
    chat = model.start_chat()

    print("Weather Assistant is ready! Ask me for the weather. Type 'quit' to exit.")

    # --- Outer loop for user input ---
    while True:
        user_query = input("\n> ")
        end_words = ['quit', 'exit', 'stop', 'cancel', 'terminate', 'finish', 'close', 'end', 'abort', 'reset', 'halt', 'pause', 'suspend']
        if user_query.lower() in end_words:
            break

        # Send the initial message
        response = chat.send_message(user_query)

        # --- Inner loop to handle multiple tool calls ---
        while True:
            try:
                # Check if the model's last response was a function call
                function_call = response.candidates[0].content.parts[0].function_call
                
                tool_name = function_call.name
                tool_args = {key: value for key, value in function_call.args.items()}
                
                print(f"AI wants to call tool: {tool_name} with arguments: {tool_args}")
                
                if tool_name == "get_city_coordinates":
                    function_response = get_city_coordinates(**tool_args)
                elif tool_name == "get_weather":
                    function_response = get_weather(**tool_args)
                else:
                    function_response = {"error": "Unknown tool called by the model."}

                # Send the result of the function call back to the AI
                response = chat.send_message(
                    [{"function_response": {"name": tool_name, "response": function_response}}]
                )

            except (IndexError, AttributeError):
                # If there is no function call, we have our final answer.
                # Print the final text response and break the inner loop.
                print(f"AI: {response.text}")
                break

if __name__ == "__main__":
    main()