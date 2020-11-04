import pytest
from api_tests.config_files import config
from api_tests.scripts.apigee_api import ApigeeDebugApi


@pytest.mark.usefixtures("setup")
class TestSpineHeadersSuite:
    """ A test suite to verify the spine headers are sent as part of the target backend request """

    @pytest.mark.spine_headers
    def test_fromASID_header_is_set(self, use_internal_testing_internal_dev_app, get_token):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_header_value = '200000001115'

        # When
        self.send_a_get_consent_request()

        # Then
        actual_header_value = debug_session.get_apigee_header('FromASID')
        assert actual_header_value == expected_header_value

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token')
    def test_ToASID_header_is_set(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        self.send_a_get_consent_request()

        # Then
        actual_header_value = debug_session.get_apigee_header('ToASID')
        assert actual_header_value is not None and actual_header_value != ''

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token')
    @pytest.mark.debug
    def test_x_request_id_equals_TraceID(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        self.send_a_get_consent_request()

        # Then
        trace_id = debug_session.get_apigee_header('TraceID')
        x_request_id = debug_session.get_apigee_header('x-request-id')

        assert trace_id == x_request_id

    def send_a_get_consent_request(self):
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
