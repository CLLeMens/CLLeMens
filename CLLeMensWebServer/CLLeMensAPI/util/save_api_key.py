from dotenv import load_dotenv, set_key, find_dotenv
from pathlib import Path
import os


def write_api_key(api_key):
    # Load existing .env file or create one if it doesn't exist
    load_dotenv()

    # Check if the API key is already present
    existing_api_key = os.getenv("OPENAI_API_KEY")
    if existing_api_key:
        print("OPENAI_API_KEY is already present, Updating...")
        set_key(find_dotenv(), "OPENAI_API_KEY", api_key)

    else:
        # Write the API key to the .env file
        set_key(find_dotenv(), "OPENAI_API_KEY", api_key)
        print("OPENAI_API_KEY has been written to the .env file.")

    # Update the environment variable in the running application
    os.environ["OPENAI_API_KEY"] = api_key

