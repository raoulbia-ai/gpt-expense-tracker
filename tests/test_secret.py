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


    # Parse the JSON string into a dictionary
    # secret_dict = json.loads(json_secret)
        
    # Access the values from the dictionary
    # token_uri = secret_dict.get('token_uri')
        
    # print(f'The API key is: {token_uri}')
    
