import pytest
from api_tests.tests.utils import Utils
from assertpy import assert_that
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
        Utils.send_request(self)

        # Then
        actual_header_value = debug_session.get_apigee_header('FromASID')        
        assert_that(expected_header_value).is_equal_to(actual_header_value)

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token')
    def test_ToASID_header_is_set(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        Utils.send_request(self)


        # Then
        actual_header_value = debug_session.get_apigee_header('ToASID')
        assert_that(actual_header_value).is_not_empty()

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token')
    @pytest.mark.debug
    def test_x_request_id_equals_TraceID(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        Utils.send_request(self)


        # Then
        trace_id = debug_session.get_apigee_header('TraceID')
        x_request_id = debug_session.get_apigee_header('x-request-id')

        assert_that(trace_id).is_equal_to(x_request_id)
