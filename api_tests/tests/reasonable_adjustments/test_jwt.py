import pytest
import jwt
import requests

from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY, REASONABLE_ADJUSTMENTS_CONSENT
from api_tests.scripts.apigee_api import ApigeeDebugApi

@pytest.mark.usefixtures("setup")
class TestJwtSuite:
    """ A test suite to check that the JWT attached to the request is valid """
        

    @pytest.mark.jwt
    @pytest.mark.usefixtures('get_token')
    def test_jwt(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY)
        expected_jwt_claims = {
            'reason_for_request': 'directcare',
            'scope': 'patient=test&category=test&status=test',
            'requesting_organization': 'https://fhir.nhs.uk/Id/ods-organization-code|D82106',
            'requesting_system': 'https://fhir.nhs.uk/Id/accredited-system|200000001115',
            'requesting_user': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'sub': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'iss': 'http://api.service.nhs.uk',
            'aud': f'/{REASONABLE_ADJUSTMENTS_PROXY}/consent'
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

        assert expected_jwt_claims['reason_for_request'] == actual_jwt_claims['reason_for_request'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['reason_for_request'], actual_jwt_claims['reason_for_request'])
        assert expected_jwt_claims['scope'] == actual_jwt_claims['scope'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['reason_for_request'], actual_jwt_claims['scope'])
        assert expected_jwt_claims['requesting_organization'] == actual_jwt_claims['requesting_organization'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['requesting_organization'], actual_jwt_claims['requesting_organization'])
        assert expected_jwt_claims['requesting_system'] == actual_jwt_claims['requesting_system'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['requesting_system'], actual_jwt_claims['requesting_system'])
        assert expected_jwt_claims['requesting_user'] == actual_jwt_claims['requesting_user'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['requesting_user'], actual_jwt_claims['requesting_user'])
        assert expected_jwt_claims['sub'] == actual_jwt_claims['sub'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['sub'], actual_jwt_claims['sub'])
        assert expected_jwt_claims['iss'] == actual_jwt_claims['iss'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['iss'], actual_jwt_claims['iss'])
        assert expected_jwt_claims['aud'] == actual_jwt_claims['aud'], 'Expected: {}, Actual: {}'.format(expected_jwt_claims['aud'], actual_jwt_claims['aud'])
