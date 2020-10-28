import pytest

from api_tests.config_files import config
from api_tests.config_files.environments import ENV
from api_tests.steps.check_oauth import CheckOauth
from api_tests.steps.check_reasonable_adjustments import CheckReasonableAdjustments

def _get_parametrized_values(request):
    for mark in request.node.own_markers:
        if mark.name == 'parametrize':
            # index 0 is the argument name while index 1 is the argument values,
            # here we are only interested in the values
            return mark.args[1]


@pytest.fixture()
def get_token(request):
    """Get the token and assign it to the test instance"""
    oauth_endpoints = CheckOauth()
    token = oauth_endpoints.get_token_response()
    setattr(request.cls, 'token', token['access_token'])
    setattr(request.cls, 'refresh', token['refresh_token'])  # This is required if you want to request a refresh token
    return oauth_endpoints


@pytest.fixture()
def get_refresh_token(request, get_token):
    """Get the refresh token and assign it to the test instance"""
    # Requesting a refresh token will expire the previous access token
    refresh_token = get_token.get_token_response(grant_type='refresh_token', refresh_token=request.cls.refresh)
    setattr(request.cls, 'refresh_token', refresh_token['refresh_token'])


@pytest.fixture(scope='function')
def update_token_in_parametrized_headers(request):
    # Manually setting this fixture for session use because the pytest
    # session scope is called before any of the markers are set.
    if not hasattr(request.cls, 'setup_done'):
        token = CheckOauth().get_token_response()
        for value in _get_parametrized_values(request):
            if value.get('Authorization', None) == 'valid_token':
                value['Authorization'] = f'Bearer {token["access_token"]}'

        # Make sure the token is not refreshed before every test
        setattr(request.cls, 'setup_done', True)


@pytest.fixture()
def use_internal_testing_internal_dev_app():
    config.CLIENT_ID = ENV['apps']['internal_testing_internal_dev']['client_id']
    config.CLIENT_SECRET = ENV['apps']['internal_testing_internal_dev']['client_secret']
    config.REDIRECT_URI = ENV['apps']['internal_testing_internal_dev']['redirect_url']


@pytest.fixture()
def use_internal_testing_internal_dev_without_asid_app():
    config.CLIENT_ID = ENV['apps']['missing_asid']['client_id']
    config.CLIENT_SECRET = ENV['apps']['missing_asid']['client_secret']
    config.REDIRECT_URI = ENV['apps']['missing_asid']['redirect_url']


@pytest.fixture()
def use_internal_testing_internal_dev_without_ods_app():
    config.CLIENT_ID = ENV['apps']['missing_ods']['client_id']
    config.CLIENT_SECRET = ENV['apps']['missing_ods']['client_secret']
    config.REDIRECT_URI = ENV['apps']['missing_ods']['redirect_url']


@pytest.fixture(scope='function')
def setup(request, use_internal_testing_internal_dev_app):
    """This function is called before each test is executed"""

    # Get the name of the current test and attach it the the test instance
    name = (request.node.name, request.node.originalname)[request.node.originalname is not None]
    setattr(request.cls, "name", name)

    oauth = CheckOauth()
    setattr(request.cls, "oauth", oauth)

    reasonable_adjustments = CheckReasonableAdjustments()
    setattr(request.cls, "reasonable_adjustments", reasonable_adjustments)

    yield  # Handover to test

    # Teardown
    try:
        # Close any lingering sessions
        request.cls.test.session.close()
    except AttributeError:
        # Probably failed during setup
        # so nothing to teardown
        pass
