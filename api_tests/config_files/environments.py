import os


# Configure Test Environment
def get_env(variable_name: str, default: str = "") -> str:
    """Returns a environment variable"""
    try:
        return os.environ[variable_name]
    except KeyError:
        return default


ENV = {
    'oauth': {
        'apigee_client_id': get_env('APIGEE_CLIENT_ID'),
        'base_url': get_env('BASE_URL'),
        'client_id': get_env('CLIENT_ID'),
        'client_secret': get_env('CLIENT_SECRET'),
        'redirect_uri': get_env('REDIRECT_URI'),
        'authenticate_url': get_env('AUTHENTICATE_URL'),
    },
    'apigee': {
        'base_url': get_env('APIGEE_API_URL'),
        'api_authentication': get_env('APIGEE_API_AUTHENTICATION'),
    },
    'reasonable_adjustments': {
        'base_url': get_env('REASONABLE_ADJUSTMENTS_BASE_URL'),
        'proxy_name': get_env('REASONABLE_ADJUSTMENTS_PROXY'),
    }
}