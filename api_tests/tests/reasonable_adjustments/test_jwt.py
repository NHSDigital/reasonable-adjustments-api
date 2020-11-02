import pytest
import jwt
import requests

from assertpy import assert_that
from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY_NAME, REASONABLE_ADJUSTMENTS_PROXY_PATH, REASONABLE_ADJUSTMENTS_CONSENT
from api_tests.scripts.apigee_api import ApigeeDebugApi

@pytest.mark.usefixtures("setup")
class TestJwtSuite:
    """ A test suite to check that the JWT attached to the request is valid """
        

    @pytest.mark.jwt
    @pytest.mark.usefixtures('get_token')
    def test_jwt(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_jwt_claims = {
            'reason_for_request': 'directcare',
            'scope': 'patient=test&category=test&status=test',
            'requesting_organization': 'https://fhir.nhs.uk/Id/ods-organization-code|D82106',
            'requesting_system': 'https://fhir.nhs.uk/Id/accredited-system|200000001115',
            'requesting_user': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'sub': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'iss': 'http://api.service.nhs.uk',
            'aud': f'/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/consent'
        }

        # When
        requests.get(
            url=REASONABLE_ADJUSTMENTS_CONSENT,
            params={'patient': 'test', 'category': 'test', 'status': 'test'},
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
            }
        )

        # Then
        actual_jwt = debug_session.get_apigee_header('jwt')
        actual_jwt_claims = jwt.decode(actual_jwt, verify=False)

        assert_that(expected_jwt_claims['reason_for_request']).is_equal_to_ignoring_case(actual_jwt_claims['reason_for_request'])
        assert_that(expected_jwt_claims['scope']).is_equal_to_ignoring_case(actual_jwt_claims['scope'])
        assert_that(expected_jwt_claims['requesting_organization']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_organization'])
        assert_that(expected_jwt_claims['requesting_system']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_system'])
        assert_that(expected_jwt_claims['requesting_user']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_user'])
        assert_that(expected_jwt_claims['sub']).is_equal_to_ignoring_case(actual_jwt_claims['sub'])
        assert_that(expected_jwt_claims['iss']).is_equal_to_ignoring_case(actual_jwt_claims['iss'])
        assert_that(expected_jwt_claims['aud']).is_equal_to_ignoring_case(actual_jwt_claims['aud'])
