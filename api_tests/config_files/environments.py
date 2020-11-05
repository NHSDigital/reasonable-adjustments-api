import os


# Configure Test Environment
def get_env(variable_name: str, default: str = "") -> str:
    """Returns a environment variable"""
    try:
        return os.environ[variable_name]
    except KeyError:
        return default


ENV = {
    'apps': {
        'internal_testing_internal_dev': {
            'client_id': get_env('CLIENT_ID'),
            'client_secret': get_env('CLIENT_SECRET'),
            'redirect_url': get_env('REDIRECT_URI')
        },
        'missing_asid': {
            'client_id': get_env('MISSING_ASID_CLIENT_ID'),
            'client_secret': get_env('MISSING_ASID_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        },
        'missing_ods': {
            'client_id': get_env('MISSING_ODS_CLIENT_ID'),
            'client_secret': get_env('MISSING_ODS_CLIENT_SECRET'),
            'redirect_url': 'https://example.com/callback'
        }
    },
    'oauth': {
        'apigee_client_id': get_env('APIGEE_CLIENT_ID'),
        'base_url': get_env('BASE_URL'),
        'client_id': get_env('CLIENT_ID'),
        'client_secret': get_env('CLIENT_SECRET'),
        'redirect_uri': get_env('REDIRECT_URI'),
        'authenticate_url': get_env('AUTHENTICATE_URL'),
    },
    'apigee': {
        'organisation': get_env('APIGEE_ORGANISATION'),
        'base_url': get_env('APIGEE_API_URL'),
        'api_authentication': get_env('APIGEE_API_AUTHENTICATION'),
        'username': get_env('APIGEE_USERNAME'),
        'password': get_env('APIGEE_PASSWORD'),
    },
    'reasonable_adjustments': {
        'base_url': get_env('REASONABLE_ADJUSTMENTS_BASE_URL'),
        'proxy_path': get_env('REASONABLE_ADJUSTMENTS_PROXY_PATH'),
        'proxy_name': get_env('REASONABLE_ADJUSTMENTS_PROXY_NAME'),
    }
}