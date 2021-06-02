import pytest
import json
import requests

from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request
from api_tests.tests.utils import Utils
from api_tests.config_files import config
from assertpy import assert_that
import uuid


@pytest.mark.usefixtures("setup")
class TestErrorCaseSuite:
    """ A test suite to verify the correct error messages from an invalid request """

    @pytest.mark.errors
    @pytest.mark.integration
    def test_missing_access_token(self):
        # Given
        expected_status_code = 401
        expected_response = {
            "error": "access token is invalid or expired",
            "error_description": "access token is invalid or expired"
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
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_missing_x_request_id_header(self):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'request',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'INVALID_REQUEST',
                                'display': 'invalid header'
                            }
                        ]
                    },
                    'diagnostics': 'x-request-id is missing or invalid'
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
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_invalid_x_request_id_header(self):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error',
                    'code': 'request',
                    'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': 'INVALID_REQUEST',
                                'display': 'invalid header'
                            }
                        ]
                    },
                    'diagnostics': 'x-request-id is missing or invalid'
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
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
    @pytest.mark.usefixtures('get_token_internal_dev')
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
                             
    def test_missing_nhsd_session_urid_header(self, nhsd_session_urid):
        # Given
        expected_status_code = 400
        expected_response = {
            'resourceType': 'OperationOutcome',
            'issue':
            [
                {
                    'severity': 'error', 'code': '400', 'details':
                    {
                        'coding':
                        [
                            {
                                'system': 'https://fhir.nhs.uk/R4/CodeSystem/Spine-ErrorOrWarningCode',
                                'version': '1',
                                'code': '400',
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
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
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
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_invalid_content_type(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "content-type must be set to application/fhir+json"
        }

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            headers={
                'Authorization': f'Bearer {self.token}',
                'x-request-id': str(uuid.uuid4()),
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'content-type': 'application/json'
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_invalid_payload(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid request payload",
            "error_description": "requires payload"
        }

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            headers={
                'Authorization': f'Bearer {self.token}',
                'x-request-id': str(uuid.uuid4()),
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'content-type': 'application/fhir+json'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    @pytest.mark.parametrize('url,params', [(config.REASONABLE_ADJUSTMENTS_CONSENT, {'patient': 'test', 'category': 'test'}),
                                            (config.REASONABLE_ADJUSTMENTS_LIST, {'patient': 'test', 'code': 'test'}),
                                            (config.REASONABLE_ADJUSTMENTS_FLAG, {'patient': 'test', 'category': 'test'})])
    def test_get_invalid_query_params(self, url, params):
        # Given
        expected_status_code = 404
        expected_response = {
            'error': 'invalid query parameters',
            'error_description': 'required query parameters are missing or have empty values'
        }

        # When
        response = requests.get(
            url,
            params,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_invalid_header_put(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "if-match is missing or invalid",
        }

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            },
            data={
                'message': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_invalid_query_params(self):
        # Given
        expected_status_code = 404
        expected_response = {
            'error': 'invalid query parameters',
            'error_description': 'required query parameters are missing or have empty values'
        }

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            params={
                'patient':  'test',
                'code': '',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_invalid_header_put(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "if-match is missing or invalid"
        }

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_removerarecord_invalid_header_post(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "if-match is missing or invalid"
        }

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.ods
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_missing_ods')
    def test_missing_ods(self):
        # Given
        expected_status_code = 500
        expected_response = {
            'error': 'missing ODS',
            'error_description': 'An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID',
        }

        # When
        response = Utils.send_request(self)
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.asid
    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_missing_asid')
    def test_missing_asid(self):
        # Given
        expected_status_code = 500
        expected_response = {
            'error': 'missing ASID',
            'error_description': 'An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID',
        }

        # When
        response = Utils.send_request(self)

        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(
            actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.integration
    def test_invalid_url(self):
        # Given
        expected_status_code = 404
        expected_response = {
            'error': "Resource Not Found"
        }

        # When
        response = requests.get(url=config.REASONABLE_ADJUSTMENTS_BASE_URL + '/' +
                                config.REASONABLE_ADJUSTMENTS_PROXY_PATH + '/test')
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])

    @pytest.mark.errors
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_duplicate_consent_record(self):
        # Pre-Req
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 422

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': '093895563513',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        response_body = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that('duplicate').is_equal_to(response_body['issue'][0]['code'])
