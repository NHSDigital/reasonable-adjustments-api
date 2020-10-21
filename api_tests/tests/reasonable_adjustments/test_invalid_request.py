from api_tests.config_files import config
import pytest
import json

@pytest.mark.usefixtures("setup")
class TestInvalidRequestSuite:
    """ A test suite to verify the correct error messages from an invalid request """

    @pytest.mark.errors
    def test_missing_access_token(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=401,
            expected_response={
                "error": "access token is invalid or expired",
                "error_description": "access token is invalid or expired"
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_missing_x_request_id_header(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=400,
            expected_response={
                "error": "invalid header",
                "error_description": "x-request-id is missing or invalid"
            },
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
    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_missing_nhsd_session_urid_header(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=400,
            expected_response={
                "error": "invalid header",
                "error_description": "nhsd-session-urid is missing or invalid"
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_invalid_content_type(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='consent',
            expected_status_code=400,
            expected_response={
                "error": "invalid header",
                "error_description": "content-type must be set to application/fhir+json"
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_invalid_payload(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='consent',
            expected_status_code=400,
            expected_response={
                "error": "invalid request payload",
                "error_description": "requires payload"
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'x-request-id': 'test',
                'nhsd-session-urid': 'test',
                'content-type': 'application/fhir+json'
            }
        )

    ## TODO: Implment mock endpoint that returns 500 response to test DefaultFaultRule
    # @pytest.mark.errors
    # @pytest.mark.usefixtures('get_token')
    # def test_unkown_error(self):
    #     assert self.reasonable_adjustments.check_endpoint(
    #         verb='POST',
    #         endpoint='consent',
    #         expected_status_code=500,
    #         expected_response={
    #             "error": "unknown_error",
    #             "error_description": "An unknown error occurred processing this request. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID"
    #         },
    #         headers={
    #             'Authorization': f'Bearer {self.token}',
    #             'x-request-id': 'test',
    #             'nhsd-session-urid': 'test',
    #             'content-type': 'application/fhir+json'
    #         },
    #         data={
    #             'message': 'test'
    #         }
    #     )

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_consent_invalid_query_params(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='consent',
            expected_status_code=404,
            expected_response={
                'error': 'invalid query parameters',
                'error_description': 'required query parameters are missing or have empty values'
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_flag_invalid_query_params(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='flag',
            expected_status_code=404,
            expected_response={
                'error': 'invalid query parameters',
                'error_description': 'required query parameters are missing or have empty values'
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_flag_invalid_header_put(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            expected_status_code=400,
            expected_response={
                "error": "invalid header",
                "error_description": "if-match is missing or invalid",
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test'
            },
            data={
                'message': 'test'
            }
        )

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_list_invalid_query_params(self):
        # Test list endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='list',
            expected_status_code=404,
            expected_response={
                'error': 'invalid query parameters',
                'error_description': 'required query parameters are missing or have empty values'
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_list_invalid_header_put(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            expected_status_code=400,
            expected_response={
                "error": "invalid header",
                "error_description": "if-match is missing or invalid",
            },
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

    @pytest.mark.errors
    @pytest.mark.usefixtures('get_token')
    def test_remove_ra_record_invalid_query_params(self):
        # Test list endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='remove_ra_record',
            expected_status_code=404,
            expected_response={
                'error': 'invalid query parameters',
                'error_description': 'required query parameters are missing or have empty values'
            },
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
