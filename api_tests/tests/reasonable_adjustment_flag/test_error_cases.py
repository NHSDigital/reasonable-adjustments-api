import pytest
import json
import requests
from pytest_nhsd_apim.apigee_apis import ApigeeNonProdCredentials, ApigeeClient, DeveloperAppsAPI

from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request
from api_tests.tests.utils import Utils
from api_tests.tests.conftest import ASID_ONLY_ATTR, ODS_ONLY_ATTR
from assertpy import assert_that
import uuid


class TestErrorCaseSuite:
    """ A test suite to verify the correct error messages from an invalid request """

    @pytest.mark.errors
    @pytest.mark.integration
    def test_missing_access_token(self, nhsd_apim_proxy_url):
        # Given
        expected_status_code = 401
        expected_diagnostic = 'Access token is invalid or expired'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
                '_from': 'json'
            },
            headers={
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_missing_x_request_id_header(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'x-request-id is missing or invalid'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
                '_from': 'json'
            },
            headers={**nhsd_apim_auth_headers, 'accept': 'application/fhir+json'}
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_invalid_x_request_id_header(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'x-request-id is missing or invalid'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
                '_from': 'json'
            },
            headers={**nhsd_apim_auth_headers,
                'accept': 'application/fhir+json',
                'x-request-id': 'not-GUID'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    @pytest.mark.parametrize('nhsd_session_urid',
                             [
                                 # Empty string
                                 (''),

                                 # Invalid nhsd-session-urid
                                 ('This is not a valid nhsd-session-urid'),

                                 # Symbols
                                 ('#£$?!&%*.;@~_-'),

                                 # Numbers
                                 ('0123456789')
                             ]
                             )
    def test_missing_nhsd_session_urid_header(self, nhsd_session_urid, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'nhsd-session-urid is invalid'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
                '_from': 'json'
            },
            headers={**nhsd_apim_auth_headers,
                'accept': 'application/fhir+json',
                'x-request-id': str(uuid.uuid4()),
                'nhsd-session-urid': nhsd_session_urid,
            }
        )

        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_invalid_content_type(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'content-type must be set to application/fhir+json'

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/json'
            },
            json=request_bank.get_body(Request.CONSENT_POST)
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_invalid_payload(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'requires payload'

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])


    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    @pytest.mark.parametrize('endpoint, params', [
        ("/Consent", {'patient': 'test', 'category': 'test'}),
        ("/List", {'patient': 'test', 'code': 'test'}),
        ("/Flag", {'patient': 'test', 'category': 'test'})
    ])
    def test_get_invalid_query_params(self, endpoint, params, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_diagnostic = 'required query parameters are missing or have empty values'

        # When
        response = requests.get(
            url=nhsd_apim_proxy_url + endpoint,
            params=params,
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_flag_invalid_header_put(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes):
        # Pre-Req: Patient has both a consent and flag
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        Utils.send_flag_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        get_flag_response = Utils.send_flag_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Given
        expected_status_code = 400
        expected_diagnostic = 'if-match is missing or invalid'
        flag_id = get_flag_response['id']
        version_id = get_flag_response['version']

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/Flag/{flag_id}",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
                'If-match': version_id,
            },
            json=request_bank.get_body(Request.FLAG_PUT)
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_list_invalid_query_params(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_diagnostic = 'required query parameters are missing or have empty values'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/List",
            params={
                'patient': 'test',
                'code': '',
                'status': 'test',
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_list_invalid_header_put(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes):
        # Pre-Req
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        Utils.send_list_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        get_list_response = Utils.send_list_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        list_id = get_list_response['id']

        # Given
        expected_status_code = 400
        expected_diagnostic = 'if-match is missing or invalid'

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/List/{list_id}",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'accept': 'application/fhir+json',
                'if-match': '',
            },
            json=request_bank.get_body(Request.LIST_PUT)
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_removerarecord_invalid_header_post(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_diagnostic = 'if-match is missing or invalid'

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/$removerarecord",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': ''
            },
            json=request_bank.get_body(Request.REMOVE_RA_RECORD_POST)
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.ods
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    @pytest.mark.skip(
        "This test passes when run individually, but fails as part of a session. This is likely due to us trying"
        "to change the test app attributes per-test whilst the nhsd_apim_test_app fixture is session-scoped."
    )
    def test_missing_ods(self, test_app_with_asid_only, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 500
        expected_diagnostic = 'An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': 'test',
                'status': 'test',
                'category': 'test',
            },
            headers={**nhsd_apim_auth_headers,
                'accept': 'application/fhir+json',
                'x-request-id': str(uuid.uuid4()),
            }
        )
        # import pdb; pdb.set_trace()
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.asid
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    @pytest.mark.skip(
        "This test passes when run individually, but fails as part of a session. This is likely due to us trying"
        "to change the test app attributes per-test whilst the nhsd_apim_test_app fixture is session-scoped."
    )
    def test_missing_asid(self, test_app_with_ods_only, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 500
        expected_diagnostic = 'An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID'

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': 'test',
                'category': 'test',
                'status': 'test',
            },
            headers={**nhsd_apim_auth_headers,
                'accept': 'application/fhir+json',
                'x-request-id': str(uuid.uuid4()),
            }
        )

        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    def test_invalid_url(self, nhsd_apim_proxy_url):
        # Given
        expected_status_code = 404
        expected_diagnostic = 'Resource Not Found'

        # When
        response = requests.get(url=f"{nhsd_apim_proxy_url}/invalid")
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to_ignoring_case(actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    # @pytest.mark.skip(
    #     "Skipped due to backend returning invalid/missing header error response for POST requests to /Consent, "
    #     "needs further looking into."
    # )
    def test_duplicate_consent_record(self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes):
        # Pre-Req
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 422
        expected_diagnostic = 'The patient already has an active consent'

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'x-correlation-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )

        response_body = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_diagnostic).is_equal_to(response_body['issue'][0]['diagnostics'])
