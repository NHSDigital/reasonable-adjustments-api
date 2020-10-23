import pytest
import json
from api_tests.config_files import config
from api_tests.scripts.apigee_api import ApigeeDebugApi


@pytest.mark.usefixtures("setup")
class TestInteractionIDSuite:
    """ A test suite to verify the interactionID is fetched from KVM """

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_consent_get(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Consent.read:1'

        # When
        self.send_a_get_consent_request()

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')
        assert actual_interaction_id == expected_interaction_id

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

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_consent_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Consent.write:1'

        # When
        self.send_a_put_consent_request()

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')
        assert actual_interaction_id == expected_interaction_id

    def send_a_put_consent_request(self):
        self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_CONSENT + '/1',
            expected_status_code=200,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_flag_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Flag.write:1'

        # When
        self.send_a_put_flag_request()

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')
        assert actual_interaction_id == expected_interaction_id

    def send_a_put_flag_request(self):
        self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            expected_status_code=200,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_list_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:List.write:1'

        # When
        self.send_a_put_list_request()

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')
        assert actual_interaction_id == expected_interaction_id

    def send_a_put_list_request(self):
        self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            expected_status_code=200,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )
