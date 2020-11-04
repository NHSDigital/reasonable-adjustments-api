import pytest
import json
import requests
from api_tests.scripts.apigee_api import ApigeeDebugApi
from api_tests.tests.utils import Utils
from api_tests.config_files import config
from assertpy import assert_that


@pytest.mark.usefixtures("setup")
class TestErrorCaseSuite:
    """ A test suite to verify the correct error messages from an invalid request """

    @pytest.mark.errors
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
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_missing_x_request_id_header(self):
        # Given
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "x-request-id is missing or invalid"
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
                'nhsd-session-urid': 'test',
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])
        
    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_missing_nhsd_session_urid_header(self):
        # Given 
        expected_status_code = 400
        expected_response = {
            "error": "invalid header",
            "error_description": "nhsd-session-urid is missing or invalid"
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
                'x-request-id': 'test',
                'nhsd-session-urid': '',
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_invalid_content_type(self):
        # Given
        expected_status_code = 400
        expected_response={
            "error": "invalid header",
            "error_description": "content-type must be set to application/fhir+json"
        }

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            headers={
                'Authorization': f'Bearer {self.token}',
                'x-request-id': 'test',
                'nhsd-session-urid': 'test',
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
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_invalid_payload(self):
        # Given
        expected_status_code = 400
        expected_response={
            "error": "invalid request payload",
            "error_description": "requires payload"
        }

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            headers={
                'Authorization': f'Bearer {self.token}',
                'x-request-id': 'test',
                'nhsd-session-urid': 'test',
                'content-type': 'application/fhir+json'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_consent_invalid_query_params(self):
        # Given
        expected_status_code = 404
        expected_response={
            'error': 'invalid query parameters',
            'error_description': 'required query parameters are missing or have empty values'
        }

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_flag_invalid_query_params(self):
        # Given
        expected_status_code = 404
        expected_response={
            'error': 'invalid query parameters',
            'error_description': 'required query parameters are missing or have empty values'
        }

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])
    

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_flag_invalid_header_put(self):
        # Given
        expected_status_code = 400
        expected_response={
            "error": "invalid header",
            "error_description": "if-match is missing or invalid",
        }

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
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
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
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
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_list_invalid_header_put(self):
        # Given
        expected_status_code=400
        expected_response={
            "error": "invalid header",
            "error_description": "if-match is missing or invalid"
        }
        
        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
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
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_remove_ra_record_invalid_query_params(self):
        # Given
        expected_status_code = 404
        expected_response = {
            'error': 'invalid query parameters',
            'error_description': 'required query parameters are missing or have empty values'
        }

        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            params={
                'patient':  'test',
                'removalReason': '',
                'supportingComment': 'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )
        actual_response = json.loads(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(actual_response['message_id']).is_not_empty()
        assert_that(expected_response['error']).is_equal_to_ignoring_case(actual_response['error'])
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.ods
    @pytest.mark.errors
    def test_missing_ods(self, use_internal_testing_internal_dev_without_ods_app, get_token):
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
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])

    @pytest.mark.asid
    @pytest.mark.errors
    def test_missing_asid(self, use_internal_testing_internal_dev_without_asid_app, get_token):
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
        assert_that(expected_response['error_description']).is_equal_to_ignoring_case(actual_response['error_description'])