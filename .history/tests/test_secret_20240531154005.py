"""script to test reading secrests stored in the Github repository settings."""

import os
import json

# use .env file
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


# Get the JSON string from the environment variable
json_secret = os.getenv('AZURE_TENANT')

if json_secret is None:
    print("JSON secret not found. Please check your environment variable configuration.")
else:
    
    print(json_secret)
    
