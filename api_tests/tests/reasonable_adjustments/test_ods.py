import pytest

from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY
from api_tests.scripts.apigee_api import ApigeeDebugApi


@pytest.mark.usefixtures("setup")
class TestAsidSuite:
    """ A test suit to verify ODS is fetched from Custom Attributes associated with the App """

    @pytest.mark.ods
    @pytest.mark.usefixtures('get_token')
    def test_ods(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY)
        expected_ods = 'D82106'

        # When
        self.send_a_request()

        # Then
        actual_ods = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
        assert actual_ods == expected_ods

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
