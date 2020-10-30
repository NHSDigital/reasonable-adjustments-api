import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Configure Test Environment
# def get_env(variable_name: str, default: str = "") -> str:
#     """Returns a environment variable"""
#     try:
#         return os.environ[variable_name]
#     except KeyError:
#         return default


ENV = {
    'apps': {
        'internal_testing_internal_dev': {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET'),
            'redirect_url': os.environ.get('REDIRECT_URI')
        },
        'missing_asid': {
            'client_id': os.environ.get('MISSING_ASID_CLIENT_ID'),
            'client_secret': os.environ.get('MISSING_ASID_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        },
        'missing_ods': {
            'client_id': os.environ.get('MISSING_ODS_CLIENT_ID'),
            'client_secret': os.environ.get('MISSING_ODS_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        }
    },
    'oauth': {
        'apigee_client_id': os.environ.get('APIGEE_CLIENT_ID'),
        'base_url': os.environ.get('BASE_URL'),
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'redirect_uri': os.environ.get('REDIRECT_URI'),
        'authenticate_url': os.environ.get('AUTHENTICATE_URL'),
    },
    'apigee': {
        'organisation': os.environ.get('APIGEE_ORGANISATION'),
        'base_url': os.environ.get('APIGEE_API_URL'),
        'api_authentication': os.environ.get('APIGEE_API_AUTHENTICATION'),
        'username': os.environ.get('APIGEE_USERNAME'),
        'password': os.environ.get('APIGEE_PASSWORD'),
    },
    'reasonable_adjustments': {
        'base_url': os.environ.get('REASONABLE_ADJUSTMENTS_BASE_URL'),
        'proxy_path': os.environ.get('REASONABLE_ADJUSTMENTS_PROXY_PATH'),
        'proxy_name': os.environ.get('REASONABLE_ADJUSTMENTS_PROXY_NAME'),
    }
}