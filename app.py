from flask import Flask, request, jsonify, abort
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import logging
import base64

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# API Key for authentication
API_KEY = os.getenv('MY_API_KEY')
app.logger.debug(f"Loaded API Key: {API_KEY}")

# Google Sheets Configuration
def get_google_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_path = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT_SECRET')
        if not creds_path:
            app.logger.error("Google Sheets service account secret not found. Make sure GOOGLE_SHEETS_SERVICE_ACCOUNT_SECRET is set.")
            return None
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open("groceries_shopping").sheet1
        app.logger.info("Successfully accessed Google Sheet: groceries_shopping")
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        app.logger.error("Spreadsheet not found. Please check the name 'groceries_shopping'.")
        return None
    except gspread.exceptions.APIError as api_err:
        app.logger.error(f"Google API error: {api_err}")
        return None
    except Exception as e:
        app.logger.error(f"An unexpected error occurred while accessing Google Sheet: {e}")
        return None

# Decorator to require API key via Basic Auth
def require_api_key(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        app.logger.debug(f"Authorization header received: {auth_header}")
        if auth_header:
            auth_type, credentials = auth_header.split()
            if auth_type == 'Basic':
                decoded_credentials = base64.b64decode(credentials).decode('utf-8')
                app.logger.debug(f"Decoded credentials: {decoded_credentials}")
                try:
                    api_key, dummy = decoded_credentials.split(':')
                    app.logger.debug(f"Received API Key: {api_key}")
                except ValueError:
                    app.logger.warning("Invalid credentials format.")
                    abort(401)
                if api_key == API_KEY:
                    return func(*args, **kwargs)
                else:
                    app.logger.warning("API Key mismatch.")
        app.logger.warning("Unauthorized access attempt.")
        abort(401)
    return wrapper

@app.route('/')
def index():
    return 'Welcome to the Expense Tracker App'

@app.route('/receive_payload', methods=['POST'])
@require_api_key
def receive_payload():
    try:
        app.logger.info("Received payload request")
        data = request.get_json()
        app.logger.info(f"Request data: {data}")
        rows = data.get('rows', [])

        sheet = get_google_sheet()
        if sheet is None:
            return jsonify({"error": "Failed to access Google Sheet"}), 500
        
        for row in rows:
            sheet.append_row([row['Date'], row['Shop'], row['Item'], row['Price'], row['Category']])

        response = jsonify({"status": "success"})
        app.logger.info(f"Response: {response.get_json()}")
        return response, 200
    except Exception as e:
        app.logger.error(f"Receive payload error: {e}")
        return jsonify({"error": "Failed to process payload"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
