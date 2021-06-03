import pytest
import time

from api_tests.config_files import config
from api_tests.steps.check_oauth import CheckOauth
from api_tests.tests.utils import Utils


def _get_parametrized_values(request):
    for mark in request.node.own_markers:
        if mark.name == 'parametrize':
            # index 0 is the argument name while index 1 is the argument values,
            # here we are only interested in the values
            return mark.args[1]


@pytest.fixture()
def get_token_internal_dev(request):
    if 'sandbox' in config.REASONABLE_ADJUSTMENTS_BASE_URL:
        # auth token is not required when executing against sandbox
        setattr(request.cls, 'token', None)
        setattr(request.cls, 'sandbox', True)
    else:
        setattr(request.cls, 'sandbox', False)
        return _get_token(request, config.INTERNAL_TESTING_INTERNAL_DEV)


@pytest.fixture()
def get_token_missing_ods(request):
    return _get_token(request, config.MISSING_ODS)


@pytest.fixture()
def get_token_missing_asid(request):
    return _get_token(request, config.MISSING_ASID)


def _get_token(request, creds):
    """Get the token and assign it to the test instance"""
    oauth_endpoints = CheckOauth(creds)
    token = oauth_endpoints.get_token_response()
    setattr(request.cls, 'token', token['access_token'])
    setattr(request.cls, 'refresh', token['refresh_token'])  # This is required if you want to request a refresh token
    return oauth_endpoints


def get_refresh_token(request, get_token):
    """Get the refresh token and assign it to the test instance"""
    # Requesting a refresh token will expire the previous access token
    refresh_token = get_token.get_token_response(grant_type='refresh_token', refresh_token=request.cls.refresh)
    setattr(request.cls, 'refresh_token', refresh_token['refresh_token'])


@pytest.fixture(scope='function', autouse=True)
def setup(request):
    """This function is called before each test is executed"""

    # Get the name of the current test and attach it the the test instance
    name = (request.node.name, request.node.originalname)[request.node.originalname is not None]
    setattr(request.cls, "name", name)

    yield  # Handover to test
    time.sleep(1)

    # Teardown
    # Return patient to previous state

    if hasattr(request.cls, 'token'):
        # Call this regardless whether any flags exist
         Utils.send_raremoverecord_post(request.cls.token)

    try:
        # Close any lingering sessions
        request.cls.test.session.close()
    except AttributeError:
        # Probably failed during setup
        # so nothing to teardown
        pass
