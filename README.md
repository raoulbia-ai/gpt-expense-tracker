# Optimizing Data Capture: ChatGPT Actions, Flask API, and Google Sheets Integration

This project harnesses the power of AI to streamline the process of extracting information from an photo and inserting the data into a spreasheet. THe application uses ChatGPT Actions, a Flask-based API, and Google Sheets integration to create an efficient and user-friendly solution. The project also showcases the interactive development process with ChatGPT and the steps to integrate ChatGPT Actions with an Azure Web App. It further demonstrates the integration with Google Sheets and the use of Base64 format for secure handling of authentication headers. This GPT-powered solution has potential applications across various industries like finance, logistics, and healthcare. Explore the power of AI-driven solutions for personal and professional efficiency with this project.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9
- Docker 
- Azure infrastructure: Azure Container Registry and Azure Web App (Free Tier will do)
- Google Account and new project in Google Developer Console.

### Application Overview

#### API Key Configuration

The API key for authentication is loaded from an environment variable.

#### Google Sheets Configuration

The `get_google_sheet` function is responsible for authenticating with Google Sheets using service account credentials and opening a specific spreadsheet.

#### API Key Requirement

The application requires two keys:

* `MY_API_KEY`: this is generated by the `utils/generate_api_key.py` script. Keep it safe! The key is used intwo ways:
   * use the key to create an Azure Web App environment variable.
   * encode the key using the `utils/generate_api_key.py` script. Use the encoded API Key in your API Key configuration of the ChatGPT Custom Action.

#### Routes

`@app.route('/')`: The index route returns a welcome message. Useful for checking that the Azure web app is up and running.

`@app.route('/receive_payload', methods=['POST'])`: The receive_payload route is protected by the require_api_key 
decorator. It receives a JSON payload, processes it, and appends the data to a Google Sheet. If there's an error, it returns a JSON response with an error message.


#### Utilities

`utils/generate_api_key.py`: A utility for generating API keys.
`utils/base64_encode.py`: A utility for encoding API keys in base64.


### Running with Docker


You can build and deploy the application with the following commands:

```
docker build -t myapp:latest .
az acr login --name myacr
docker tag myapp:latest expensetrackerai.azurecr.io/myapp:latest
docker push myacr.azurecr.io/myapp:latest
```

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.

### Testing

```
curl -X POST https://mywebapp.azurewebsites.net/receive_payload \
-H "x-api-key: <unencoded-key-here>" \
-H "Content-Type: application/json" \
-d '{
    "rows": [
        {
            "Date": "2023-05-30",
            "Shop": "MarketPlace",
            "Item": "Bananas",
            "Price": 1.2,
            "Category": "Fruit"
        },
        {
            "Date": "2023-05-30",
            "Shop": "MarketPlace",
            "Item": "Chicken Breast",
            "Price": 5,
            "Category": "Meat"
        },
        {
            "Date": "2023-05-30",
            "Shop": "MarketPlace",
            "Item": "Yogurt",
            "Price": 2.5,
            "Category": "Dairy"
        }
    ]
}'
```

<br>

### Addendum: ChatGPT Actions JSON Schema

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Expense Tracker API",
    "version": "1.0.0",
    "description": "API for tracking expenses and inserting data into Google Sheets"
  },
  "servers": [
    {
      "url": "https://your-web-app-name.azurewebsites.net"
    }
  ],
  "paths": {
    "/receive_payload": {
      "post": {
        "operationId": "receivePayload",
        "summary": "Receive and process expense data",
        "description": "Receives expense data and inserts it into Google Sheets",
        "parameters": [],
        "requestBody": {
          "description": "Payload containing expense data",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "rows": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "Date": {
                          "type": "string",
                          "format": "date"
                        },
                        "Shop": {
                          "type": "string"
                        },
                        "Item": {
                          "type": "string"
                        },
                        "Price": {
                          "type": "number"
                        },
                        "Category": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "Date",
                        "Shop",
                        "Item",
                        "Price",
                        "Category"
                      ]
                    }
                  }
                },
                "required": [
                  "rows"
                ]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "Internal Server Error",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "BasicAuth": {
        "type": "http",
        "scheme": "basic"
      }
    },
    "schemas": {
      "DummyObject": {
        "type": "object",
        "properties": {
          "dummy": {
            "type": "string",
            "description": "This is a dummy object to prevent schema errors"
          }
        }
      }
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ]
}

```

Note: the `DummyObject` in components section is to prevent error "In components section, schemas subsection is not an object".