import os

import pytest as pytest
import requests as requests


@pytest.fixture()
def proxy_url():
    base_path = os.getenv("SERVICE_BASE_PATH")
    apigee_env = os.getenv("APIGEE_ENVIRONMENT")

    return f"https://{apigee_env}.api.service.nhs.uk/{base_path}"


@pytest.mark.integration
@pytest.mark.smoke
def test_ping(proxy_url):
    resp = requests.get(f"{proxy_url}/_ping")
    assert resp.status_code == 200


@pytest.mark.integration
@pytest.mark.smoke
def test_wait_for_ping(proxy_url):
    retries = 0
    resp = requests.get(f"{proxy_url}/_ping")
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != os.getenv('SOURCE_COMMIT_ID')
           and retries <= 30
           and resp.status_code == 200):
        resp = requests.get(f"{proxy_url}/_ping")
        deployed_commitId = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commitId == os.getenv('SOURCE_COMMIT_ID')


@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.happy_path
def test_status(proxy_url):
    resp = requests.get(
        f"{proxy_url}/_status", headers={"apikey": os.getenv("STATUS_ENDPOINT_API_KEY")}
    )
    assert resp.status_code == 200
    # Make some additional assertions about your status response here!


@pytest.mark.integration
@pytest.mark.smoke
def test_wait_for_status(proxy_url):
    retries = 0
    resp = requests.get(f"{proxy_url}/_status", headers={"apikey": os.getenv("STATUS_ENDPOINT_API_KEY")})
    deployed_commit_id = resp.json().get("commitId")

    while (deployed_commit_id != os.getenv('SOURCE_COMMIT_ID')
           and retries <= 30
           and resp.status_code == 200
           and resp.json().get("version")):
        resp = requests.get(f"{proxy_url}/_status", headers={"apikey": os.getenv("STATUS_ENDPOINT_API_KEY")})
        deployed_commit_id = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_commit_id == os.getenv('SOURCE_COMMIT_ID')
