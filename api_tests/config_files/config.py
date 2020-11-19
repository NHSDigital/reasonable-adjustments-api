from api_tests.config_files.environments import ENV

# Api details
APIGEE_CLIENT_ID = ENV['oauth']['apigee_client_id']
BASE_URL = ENV['oauth']['base_url']
AUTHORIZE_URL = f"{BASE_URL}/authorize"
TOKEN_URL = f"{BASE_URL}/token"

# Apigee API details
APIGEE_API_URL = ENV['apigee']['base_url']
APIGEE_AUTHENTICATION = ENV['apigee']['api_authentication']
APIGEE_ENVIRONMENT = "internal-dev"
APIGEE_USERNAME = ENV['apigee']['username']
APIGEE_PASSWORD = ENV['apigee']['password']
APIGEE_ORGANISATION = ENV['apigee']['organisation']

# Reasonable Adjustments
REASONABLE_ADJUSTMENTS_BASE_URL = ENV['reasonable_adjustments']['base_url']
REASONABLE_ADJUSTMENTS_PROXY_PATH = ENV['reasonable_adjustments']['proxy_path']
REASONABLE_ADJUSTMENTS_PROXY_NAME = ENV['reasonable_adjustments']['proxy_name']
REASONABLE_ADJUSTMENTS_CONSENT = f"{REASONABLE_ADJUSTMENTS_BASE_URL}/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/Consent"
REASONABLE_ADJUSTMENTS_FLAG = f"{REASONABLE_ADJUSTMENTS_BASE_URL}/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/Flag"
REASONABLE_ADJUSTMENTS_LIST = f"{REASONABLE_ADJUSTMENTS_BASE_URL}/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/List"
REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD = f"{REASONABLE_ADJUSTMENTS_BASE_URL}/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/$removerarecord"

# Authentication provider (Simulated OAuth)
AUTHENTICATE_URL = ENV['oauth']['authenticate_url']

# Endpoints
ENDPOINTS = {
    'authorize': AUTHORIZE_URL,
    'token': TOKEN_URL,
    'authenticate': AUTHENTICATE_URL,
    'consent': REASONABLE_ADJUSTMENTS_CONSENT,
    'flag': REASONABLE_ADJUSTMENTS_FLAG,
    'list': REASONABLE_ADJUSTMENTS_LIST,
    'remove_ra_record': REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD
}

# App details
INTERNAL_TESTING_INTERNAL_DEV = {
    'client_id': ENV['oauth']['client_id'],
    'client_secret': ENV['oauth']['client_secret'],
    'redirect_url': ENV['oauth']['redirect_uri'],
    'endpoints': ENDPOINTS
}

MISSING_ASID = {
    'client_id': ENV['apps']['missing_asid']['client_id'],
    'client_secret': ENV['apps']['missing_asid']['client_secret'],
    'redirect_url': 'https://example.com/callback',
    'endpoints': ENDPOINTS
}

MISSING_ODS = {
    'client_id': ENV['apps']['missing_ods']['client_id'],
    'client_secret': ENV['apps']['missing_ods']['client_secret'],
    'redirect_url': 'https://example.com/callback',
    'endpoints': ENDPOINTS
}

