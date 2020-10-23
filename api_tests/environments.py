import os
from dotenv import load_dotenv

load_dotenv()

# Configure Test Environment
# def get_env(variable_name: str, default: str = "") -> str:
#     """Returns a environment variable"""
#     try:
#         return os.environ[variable_name]
#     except KeyError:
#         return default

ENV = {
    'oauth': {
        'apigee_client_id': os.getenv('APIGEE_CLIENT_ID'),
        'base_url': os.getenv('BASE_URL'),
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'authenticate_url': os.getenv('AUTHENTICATE_URL'),
    },
    'apigee': {
        'organisation': os.getenv('APIGEE_ORGANISATION'),
        'base_url': os.getenv('APIGEE_API_URL'),
        'api_authentication': os.getenv('APIGEE_API_AUTHENTICATION'),
        'username': os.getenv('APIGEE_USERNAME'),
        'password': os.getenv('APIGEE_PASSWORD'),
    },
    'reasonable_adjustments': {
        'base_url': os.getenv('REASONABLE_ADJUSTMENTS_BASE_URL'),
        'proxy_name': os.getenv('REASONABLE_ADJUSTMENTS_PROXY'),
    }
}
