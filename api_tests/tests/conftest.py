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
                "jwks-resource-url":
                    "https://nhsdigital.github.io/identity-service-jwks/jwks/internal-dev/9baed6f4-1361-4a8e-8531-1f8426e3aba8.json",
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
async def get_token_client_credentials(default_oauth_helper):
    """Call identity server to get an access token"""
    # import pdb; pdb.set_trace()
    if "sandbox" in config.APIGEE_ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    id_token_jwt = default_oauth_helper.create_id_token_jwt()
    jwt = default_oauth_helper.create_jwt(kid="test-1")
    token_resp = await default_oauth_helper.get_token_response(
        grant_type="token_exchange", _jwt=jwt, id_token_jwt=id_token_jwt
    )
    import pdb; pdb.set_trace()
    return token_resp["body"]


@pytest.fixture()
@pytest.mark.parametrize('oauth_helper', [config.MISSING_ODS], indirect=True)
async def get_token_missing_ods(oauth_helper):
    """Call identity server to get an access token"""
    import pdb; pdb.set_trace()
    if "sandbox" in config.APIGEE_ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = oauth_helper.create_jwt(kid="test-1")
    token_resp = await oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]


@pytest.fixture()
@pytest.mark.parametrize('oauth_helper', [config.MISSING_ASID], indirect=True)
async def get_token_missing_asid(oauth_helper):
    """Call identity server to get an access token"""
    import pdb; pdb.set_trace()
    if "sandbox" in config.APIGEE_ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = oauth_helper.create_jwt(kid="test-1")
    token_resp = await oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]
