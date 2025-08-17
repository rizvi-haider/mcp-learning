import os
from dotenv import load_dotenv

# This line loads the variables from your .env file
load_dotenv()

# This line retrieves the specific key
api_key = os.getenv("GEMINI_API_KEY")

# Let's see if it worked!
print(api_key)