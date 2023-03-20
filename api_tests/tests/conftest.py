import time
import pytest
import asyncio
from api_tests.tests.utils import Utils
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
def test_app_with_asid_only(nhsd_apim_test_app):
    update_test_app(nhsd_apim_test_app, ASID_ONLY_ATTR)


@pytest.fixture(scope="function")
def test_app_with_ods_only(nhsd_apim_test_app):
    update_test_app(nhsd_apim_test_app, ODS_ONLY_ATTR)


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
