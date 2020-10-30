import pytest
import requests
import json
from assertpy import assert_that
from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY_NAME, REASONABLE_ADJUSTMENTS_CONSENT
from api_tests.scripts.apigee_api import ApigeeDebugApi


@pytest.mark.usefixtures("setup")
class TestOdsSuite:
    """ A test suit to verify ODS is fetched from Custom Attributes associated with the App """

    @pytest.mark.ods
    @pytest.mark.usefixtures('get_token')
    def test_valid_ods(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_ods = 'D82106'

        # When
        requests.get(
            url=REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            }
        )

        # Then
        actual_ods = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')

        assert_that(expected_ods).is_equal_to(actual_ods)

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
        response = requests.get(
            url=REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test',
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
