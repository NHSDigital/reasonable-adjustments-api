import pytest
import json
import requests
from api_tests.config_files import config
from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_PROXY_NAME, REASONABLE_ADJUSTMENTS_PROXY_PATH
from api_tests.scripts.apigee_api import ApigeeDebugApi
from api_tests.tests.utils import Utils
from assertpy import assert_that
import uuid
import base64

@pytest.mark.usefixtures("setup")
class TestHappyCasesSuite:
    """ A test suite to verify all the happy path oauth endpoints """

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_get(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient': 'test',
                'category': 'test',
                'status': 'test'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            json=json.dumps({'message': 'test'}),
            headers= {
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_put(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT + '/test',
            data=json.dumps({'message': 'test'}),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_get(self):

        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            params={
                'patient': 'test',
                'category': 'test',
                'status': 'test'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            },
            json=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_put(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_get(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            params={
                'patient':  'test',
                'code': 'test',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            },
            json=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)


    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_put(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.smoke
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_remove_ra_record_post(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            params={
                'patient': 'test',
                'removalReason': 'test',
                'supportingComment': 'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
            },
            json=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_fromASID_header_is_set(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_header_value = '200000001115'

        # When
        Utils.send_request(self)

        # Then
        actual_header_value = debug_session.get_apigee_header('FromASID')
        assert_that(expected_header_value).is_equal_to(actual_header_value)

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_ToASID_header_is_set(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        Utils.send_request(self)


        # Then
        actual_header_value = debug_session.get_apigee_header('ToASID')
        assert_that(actual_header_value).is_not_empty()

    @pytest.mark.spine_headers
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_x_request_id_equals_TraceID(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)

        # When
        Utils.send_request(self)


        # Then
        trace_id = debug_session.get_apigee_header('TraceID')
        x_request_id = debug_session.get_apigee_header('x-request-id')

        assert_that(trace_id).is_equal_to(x_request_id)

    @pytest.mark.ods
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_valid_ods(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_ods = 'D82106'

        # When
        Utils.send_request(self)

        # Then
        actual_ods = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')

        assert_that(expected_ods).is_equal_to(actual_ods)

    @pytest.mark.asid
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_valid_asid(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_asid = '200000001115'

        # When
        Utils.send_request(self)

        # Then
        actual_asid = debug_session.get_apigee_variable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
        assert_that(expected_asid).is_equal_to(actual_asid)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_interaction_id_consent_get(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Consent.read:1'

        # When
        requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient':  'test',
                'category': 'test',
                'status':   'test',
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_interaction_id_consent_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Consent.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_interaction_id_flag_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Flag.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_interaction_id_list_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_interaction_id = 'urn:nhs:names:services:raflags:List.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.jwt
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_jwt(self):
        # Given
        debug_session = ApigeeDebugApi(REASONABLE_ADJUSTMENTS_PROXY_NAME)
        expected_jwt_claims = {
            'reason_for_request': 'directcare',
            'scope': 'user/Consent.read',
            'requesting_organization': 'https://fhir.nhs.uk/Id/ods-organization-code|D82106',
            'requesting_system': 'https://fhir.nhs.uk/Id/accredited-system|200000001115',
            'requesting_user': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'sub': 'https://fhir.nhs.uk/Id/sds-role-profile-id|test',
            'iss': 'http://api.service.nhs.uk',
            'aud': f'/{REASONABLE_ADJUSTMENTS_PROXY_PATH}/Consent'
        }

        # When
        Utils.send_request(self)

        # Then
        # We should pull Authorization header instead but Apigee mask that value so we get spineJwt variable instead
        actual_jwt = debug_session.get_apigee_variable('spineJwt')

        # We manually decode jwt because, jwt library requires all three segments but we only have two (no signature).
        jwt_segments = actual_jwt.split('.')
        actual_jwt_claims = json.loads(base64.b64decode(jwt_segments[1]))

        assert_that(expected_jwt_claims['reason_for_request']).is_equal_to_ignoring_case(actual_jwt_claims['reason_for_request'])
        assert_that(expected_jwt_claims['scope']).is_equal_to_ignoring_case(actual_jwt_claims['scope'])
        assert_that(expected_jwt_claims['requesting_organization']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_organization'])
        assert_that(expected_jwt_claims['requesting_system']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_system'])
        assert_that(expected_jwt_claims['requesting_user']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_user'])
        assert_that(expected_jwt_claims['sub']).is_equal_to_ignoring_case(actual_jwt_claims['sub'])
        assert_that(expected_jwt_claims['iss']).is_equal_to_ignoring_case(actual_jwt_claims['iss'])
        assert_that(expected_jwt_claims['aud']).is_equal_to_ignoring_case(actual_jwt_claims['aud'])
