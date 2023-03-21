import time
import pytest
import asyncio
import requests
from api_tests.tests.utils import Utils
from .configuration import config
from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeConfig,
    AuthorizationCodeAuthenticator
)
from pytest_nhsd_apim.apigee_apis import ApigeeNonProdCredentials, ApigeeClient, DeveloperAppsAPI


DEFAULT_ATTR = {
    "attribute": [
        {"name": "asid", "value": "200000001390"},
        {"name": "ods", "value": "D82106"}
    ]
}
ASID_ONLY_ATTR = {
    "attribute": [
        {"name": "asid", "value": "200000001390"}
    ]
}
ODS_ONLY_ATTR = {
    "attribute": [
        {"name": "ods", "value": "D82106"}
    ]
}

ENVIRONMENT = config.ENVIRONMENT

MISSING_ASID_APP = {
    "CLIENT_ID": config.MISSING_ASID_CLIENT_ID,
    "CLIENT_SECRET": config.MISSING_ASID_CLIENT_SECRET
}

MISSING_ODS_APP = {
    "CLIENT_ID": config.MISSING_ODS_CLIENT_ID,
    "CLIENT_SECRET": config.MISSING_ODS_CLIENT_SECRET
}


def test_authorization_code_authenticator(_test_app_credentials, apigee_environment):
    # 1. Set your app config
    config = AuthorizationCodeConfig(
        environment=apigee_environment,
        identity_service_base_url=f"https://{apigee_environment}.api.service.nhs.uk/oauth2-mock",
        callback_url="https://example.com/callback",
        client_id=_test_app_credentials["CLIENT_ID"],
        client_secret=_test_app_credentials["CLIENT_SECRET"],
        scope="nhs-cis2",
        login_form={"username": "ra-test-user"},
    )

    # 2. Pass the config to the Authenticator
    authenticator = AuthorizationCodeAuthenticator(config=config)

    # 3. Get your token
    token_response = authenticator.get_token()
    assert "access_token" in token_response
    token = token_response["access_token"]

    return token


def update_test_app(test_app, attr: dict = DEFAULT_ATTR):
    _test_app = test_app()
    app_name = _test_app['name']

    _config = ApigeeNonProdCredentials()
    _client = ApigeeClient(config=_config)
    _app = DeveloperAppsAPI(client=_client)

    existing_attr = _app.get_app_attributes(email="apm-testing-internal-dev@nhs.net", app_name=app_name)
    # TODO - can we avoid this check by making the app fixture use the pytest function scope in place of the
    #  session scope used by the pytest-nhsd-apim default app?
    # If the existing app attributes does not contain the new app attributes, add the new attributes and update the app
    if not all(x in existing_attr['attribute'] for x in attr['attribute']):
        body = {'attribute': attr['attribute']}
        _app.post_app_attributes(email="apm-testing-internal-dev@nhs.net", app_name=app_name, body=body)

    # Force a refresh of the app to update the attributes in the session
    test_app(True)


@pytest.fixture(scope="class")
def test_app_with_attributes(nhsd_apim_test_app):
    update_test_app(nhsd_apim_test_app)


@pytest.fixture(scope="function")
def test_app_without_asid_token():
    return test_authorization_code_authenticator(MISSING_ASID_APP, ENVIRONMENT)


@pytest.fixture(scope="function")
def test_app_without_ods_token():
    return test_authorization_code_authenticator(MISSING_ODS_APP, ENVIRONMENT)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
def test_teardown(request, nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes):
    """This function is called before each test is executed"""

    # Get the name of the current test and attach it the the test instance
    name = (request.node.name, request.node.originalname)[request.node.originalname is not None]
    setattr(request.cls, "name", name)

    yield  # Handover to test
    time.sleep(1)

    # Teardown
    # Return patient to previous state
    # Call this regardless whether any flags exist
    Utils.send_raremoverecord_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

    try:
        # Close any lingering sessions
        request.cls.test.session.close()
    except AttributeError:
        # Probably failed during setup
        # so nothing to teardown
        pass
