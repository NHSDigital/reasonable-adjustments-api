import pytest

from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY_NAME
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
        self.send_a_request()

        # Then
        actual_ods = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
        assert actual_ods == expected_ods

    @pytest.mark.ods
    @pytest.mark.errors
    def test_missing_ods(self, use_internal_testing_internal_dev_without_ods_app, get_token):
        self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=500,
            expected_response={
                'error': 'missing ODS',
                'error_description': 'An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID',
            },
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

    def send_a_request(self):
        self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=200,
            expected_response=None,
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
