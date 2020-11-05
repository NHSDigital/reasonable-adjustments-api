import os
from dotenv import load_dotenv

load_dotenv()

ENV = {
    'apps': {
        'internal_testing_internal_dev': {
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'redirect_url': os.getenv('REDIRECT_URI')
        },
        'missing_asid': {
            'client_id': os.getenv('MISSING_ASID_CLIENT_ID'),
            'client_secret': os.getenv('MISSING_ASID_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        },
        'missing_ods': {
            'client_id': os.getenv('MISSING_ODS_CLIENT_ID'),
            'client_secret': os.getenv('MISSING_ODS_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        }
    },
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
        'proxy_path': os.getenv('REASONABLE_ADJUSTMENTS_PROXY_PATH'),
        'proxy_name': os.getenv('REASONABLE_ADJUSTMENTS_PROXY_NAME'),
    }
}