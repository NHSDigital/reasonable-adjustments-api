import pytest
import asyncio
import json
from api_tests.config_files import config
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.oauth_helper import OauthHelper
from api_test_utils.apigee_api_trace import ApigeeApiTraceDebug


@pytest.fixture
async def default_oauth_helper(app_credentials: dict = config.INTERNAL_TESTING_INTERNAL_DEV):
    """This fixture is automatically called once when used inside a class.
        The default app created here should not be modified by your tests.
        The default app has a default product associated.
        If your test requires specific app config then please create your own"""

    if config.APIGEE_ENVIRONMENT == "int" or config.APIGEE_ENVIRONMENT == "sandbox":
        oauth = OauthHelper(
            app_credentials['client_id'],
            app_credentials['client_secret'],
            app_credentials['redirect_uri']
        )
        yield oauth

    is_internal_env = (
        config.APIGEE_ENVIRONMENT == "internal-dev"
        or config.APIGEE_ENVIRONMENT == "internal-dev-sandbox"
        or config.APIGEE_ENVIRONMENT == "internal-qa"
        or config.APIGEE_ENVIRONMENT == "internal-qa-sandbox"
    )
    if is_internal_env:
        print("\nCreating Default App and Product..")
        apigee_product = ApigeeApiProducts()
        await apigee_product.create_new_product()
        await apigee_product.update_proxies(
            [config.REASONABLE_ADJUSTMENTS_PROXY_NAME, f"identity-service-{config.APIGEE_ENVIRONMENT}"]
        )
        await apigee_product.update_scopes(
            ["urn:nhsd:apim:app:level3:reasonable-adjustments-api"]
        )
        # Product ratelimit
        product_ratelimit = {
            f"{config.REASONABLE_ADJUSTMENTS_PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_product.update_attributes({"ratelimiting": json.dumps(product_ratelimit)})

        await apigee_product.update_environments([config.APIGEE_ENVIRONMENT])

        apigee_app = ApigeeApiDeveloperApps()
        await apigee_app.create_new_app()

        # Set default JWT Testing resource url and app ratelimit
        app_ratelimit = {
            f"{config.REASONABLE_ADJUSTMENTS_PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_app.set_custom_attributes(
            {
                "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
                                     "identity-service-jwks/main/jwks/internal-dev/"
                                     "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json",
                "ratelimiting": json.dumps(app_ratelimit),
            }
        )

        await apigee_app.add_api_product(api_products=[apigee_product.name])

        oauth = OauthHelper(
            client_id=apigee_app.client_id,
            client_secret=apigee_app.client_secret,
            redirect_uri=apigee_app.callback_url,
        )

        yield oauth

        print("\nDestroying Default App and Product..")
        await apigee_app.destroy_app()
        await apigee_product.destroy_product()


@pytest.mark.asyncio
async def test_default_oauth_helper(get_token_client_credentials):
    import pdb; pdb.set_trace()
    print()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def debug():
    """
    Import the test utils module to be able to:
        - Use the trace tool and get context variables after making a request to Apigee
    """
    return ApigeeApiTraceDebug(proxy=config.REASONABLE_ADJUSTMENTS_PROXY_NAME)


@pytest.mark.parametrize('app_credentials', [config.INTERNAL_TESTING_INTERNAL_DEV])
@pytest.fixture
async def get_token_client_credentials(default_oauth_helper, _app_credentials):
    """Call identity server to get an access token"""
    import pdb; pdb.set_trace()
    if "sandbox" in config.APIGEE_ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = default_oauth_helper.create_jwt(kid="test-1")
    token_resp = await default_oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]


# @pytest.fixture()
# @pytest.mark.parametrize('oauth_helper', [config.MISSING_ODS], indirect=True)
# async def get_token_missing_ods(oauth_helper):
#     """Call identity server to get an access token"""
#     import pdb; pdb.set_trace()
#     if "sandbox" in config.APIGEE_ENVIRONMENT:
#         # Sandbox environments don't need access_token. Return fake one
#         return {"access_token": "not_needed"}
#
#     jwt = oauth_helper.create_jwt(kid="test-1")
#     token_resp = await oauth_helper.get_token_response(
#         grant_type="client_credentials", _jwt=jwt
#     )
#     return token_resp["body"]
#
#
# @pytest.fixture()
# @pytest.mark.parametrize('oauth_helper', [config.MISSING_ASID], indirect=True)
# async def get_token_missing_asid(oauth_helper):
#     """Call identity server to get an access token"""
#     import pdb; pdb.set_trace()
#     if "sandbox" in config.APIGEE_ENVIRONMENT:
#         # Sandbox environments don't need access_token. Return fake one
#         return {"access_token": "not_needed"}
#
#     jwt = oauth_helper.create_jwt(kid="test-1")
#     token_resp = await oauth_helper.get_token_response(
#         grant_type="client_credentials", _jwt=jwt
#     )
#     return token_resp["body"]


# def _get_parametrized_values(request):
#     for mark in request.node.own_markers:
#         if mark.name == 'parametrize':
#             # index 0 is the argument name while index 1 is the argument values,
#             # here we are only interested in the values
#             return mark.args[1]
#
#
# @pytest.fixture()
# def get_token_internal_dev(request):
#     if 'sandbox' in config.REASONABLE_ADJUSTMENTS_BASE_URL:
#         # auth token is not required when executing against sandbox
#         setattr(request.cls, 'token', None)
#         setattr(request.cls, 'sandbox', True)
#     else:
#         setattr(request.cls, 'sandbox', False)
#         return _get_token(request, config.INTERNAL_TESTING_INTERNAL_DEV)
#
#
# @pytest.fixture()
# def get_token_missing_ods(request):
#     return _get_token(request, config.MISSING_ODS)
# #
# #
# @pytest.fixture()
# def get_token_missing_asid(request):
#     return _get_token(request, config.MISSING_ASID)
#
#
# def _get_token(request, creds):
#     """Get the token and assign it to the test instance"""
#     import pdb; pdb.set_trace()
#     oauth_endpoints = CheckOauth(creds)
#     token = oauth_endpoints.get_token_response()
#     setattr(request.cls, 'token', token['access_token'])
#     setattr(request.cls, 'refresh', token['refresh_token'])  # This is required if you want to request a refresh token
#     return oauth_endpoints
#
#
# def get_refresh_token(request, get_token):
#     """Get the refresh token and assign it to the test instance"""
#     # Requesting a refresh token will expire the previous access token
#     refresh_token = get_token.get_token_response(grant_type='refresh_token', refresh_token=request.cls.refresh)
#     setattr(request.cls, 'refresh_token', refresh_token['refresh_token'])
#
#
# @pytest.fixture(scope='function', autouse=True)
# def setup(request):
#     """This function is called before each test is executed"""
#
#     # Get the name of the current test and attach it the the test instance
#     name = (request.node.name, request.node.originalname)[request.node.originalname is not None]
#     setattr(request.cls, "name", name)
#
#     yield  # Handover to test
#     time.sleep(1)
#
#     # Teardown
#     # Return patient to previous state
#
#     if hasattr(request.cls, 'token'):
#         # Call this regardless whether any flags exist
#         Utils.send_raremoverecord_post(request.cls.token)
#
#     try:
#         # Close any lingering sessions
#         request.cls.test.session.close()
#     except AttributeError:
#         # Probably failed during setup
#         # so nothing to teardown
#         pass
