import pytest
import json
import requests
from pytest_nhsd_apim.apigee_apis import ApigeeNonProdCredentials, ApigeeClient, DeveloperAppsAPI

from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request
from api_tests.tests.utils import Utils
from api_tests.config_files import config
from api_tests.tests.conftest import ASID_ONLY_ATTR, ODS_ONLY_ATTR
from assertpy import assert_that
import uuid


class TestErrorCaseSuite:
    """ A test suite to verify the correct error messages from an invalid request """

    @pytest.mark.errors
    @pytest.mark.integration
    def test_missing_access_token(self):
        # Given
        expected_status_code = 401
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'forbidden',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'ACCESS DENIED',
                                'display': 'Access has been denied to process this request'
                            }
                        ]
                    },
               'diagnostics': 'Access token is invalid or expired'
                }
            ]
        }

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
     #   assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_missing_x_request_id_header(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'x-request-id is missing or invalid'
                }
            ]
        }

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={**nhsd_apim_auth_headers, 'accept': 'application/fhir+json'}
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_invalid_x_request_id_header(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'x-request-id is missing or invalid'
                }
            ]
        }

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={**nhsd_apim_auth_headers,
                'accept': 'application/fhir+json',
                'x-request-id': 'not-GUID'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
            actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
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
    def test_missing_nhsd_session_urid_header(self, nhsd_session_urid, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad Request'
                            }
                        ]
                    },
                    'diagnostics': 'nhsd-session-urid is invalid'
                }
            ]
        }

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
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
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_invalid_content_type(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'content-type must be set to application/fhir+json'
                }
            ]
        }

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/json'
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_invalid_payload(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                'diagnostics': 'requires payload'
                }
            ]
        }

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
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])


    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    @pytest.mark.parametrize('endpoint, params', [
        ("/Consent", {'patient': 'test', 'category': 'test'}),
        ("/List", {'patient': 'test', 'code': 'test'}),
        ("/Flag", {'patient': 'test', 'category': 'test'})
    ])
    def test_get_invalid_query_params(self, endpoint, params, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'required query parameters are missing or have empty values'
                }
            ]
        }

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
       # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_flag_invalid_header_put(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'MISSING_OR_INVALID_HEADER',
                                'display': 'There is a required header missing or invalid'
                            }
                        ]
                    },
                                'diagnostics': 'if-match is missing or invalid'
                }
            ]
        }

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
   #     assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_list_invalid_query_params(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'invalid',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'required query parameters are missing or have empty values'
                }
            ]
        }

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
       # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_list_invalid_header_put(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'MISSING_OR_INVALID_HEADER',
                                'display': 'There is a required header missing or invalid'
                            }
                        ]
                    },
                    'diagnostics': 'if-match is missing or invalid'
                }
            ]
        }

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/List/1",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': 'test',
                'if-match': ''
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
     #   assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    def test_removerarecord_invalid_header_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'MISSING_OR_INVALID_HEADER',
                                'display': 'There is a required header missing or invalid'
                            }
                        ]
                    },
                    'diagnostics': 'if-match is missing or invalid'
                }
            ]
        }

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/$removerarecord",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': ''
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
      #  assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.ods
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    @pytest.mark.skip(
        "This test passes when run individually, but fails as part of a session. This is likely due to us trying"
        "to change the test app attributes per-test whilst the nhsd_apim_test_app fixture is session-scoped."
    )
    def test_missing_ods(self, test_app_with_asid_only, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 500
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'INTERNAL_SERVER_ERROR',
                                'display': 'Unexpected internal server error'
                            }
                        ]
                    },
                    'diagnostics': 'An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID'
                }
            ]
        }

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
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.asid
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    @pytest.mark.skip(
        "This test passes when run individually, but fails as part of a session. This is likely due to us trying"
        "to change the test app attributes per-test whilst the nhsd_apim_test_app fixture is session-scoped."
    )
    def test_missing_asid(self, test_app_with_ods_only, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 500
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'value',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'INTERNAL_SERVER_ERROR',
                                'display': 'Unexpected internal server error'
                            }
                        ]
                    },
                    'diagnostics': 'An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID'
                }
            ]
        }

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
        # assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    def test_invalid_url(self):
        # Given
        expected_status_code = 404
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'not-found',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'BAD_REQUEST',
                                'display': 'Bad request'
                            }
                        ]
                    },
                    'diagnostics': 'Resource Not Found'
                }
            ]
        }

        # When
        response = requests.get(url=config.REASONABLE_ADJUSTMENTS_BASE_URL + '/' +
                                config.REASONABLE_ADJUSTMENTS_PROXY_PATH + '/test')
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response['resourceType']).is_equal_to_ignoring_case(actual_response['resourceType'])
        assert_that(expected_response['issue'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['code']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['code'])
        assert_that(expected_response['issue'][0]['details']['coding'][0]['display']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['details']['coding'][0]['display'])
        assert_that(expected_response['issue'][0]['diagnostics']).is_equal_to_ignoring_case(
        actual_response['issue'][0]['diagnostics'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "656005750105"},
        }
    )
    @pytest.mark.skip(
        "Skipped due to backend returning invalid/missing header error response for POST requests to /Consent, "
        "needs further looking into."
    )
    def test_duplicate_consent_record(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 422
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={**nhsd_apim_auth_headers,
                # 'nhsd-session-urid': '093895563513',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                # 'Accept': 'application/fhir+json'
            }
        )

        response_body = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that('duplicate').is_equal_to(response_body['issue'][0]['code'])
