import pytest
import requests
import json
from api_tests.tests.utils import Utils
from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY_NAME, REASONABLE_ADJUSTMENTS_CONSENT
from api_tests.scripts.apigee_api import ApigeeDebugApi
from assertpy import assert_that


@pytest.mark.usefixtures("setup")
class TestAsidSuite:
    """ A test suit to verify ASID is fetched from Custom Attributes associated with the App """

    @pytest.mark.asid
    @pytest.mark.usefixtures('get_token')
    def test_valid_asid(self, get_token):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_asid = '200000001115'

        # When
        Utils.send_request(self)

        # Then
        actual_asid = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
        assert_that(expected_asid).is_equal_to(actual_asid)

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
