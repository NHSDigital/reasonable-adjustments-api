import pytest
import json
import requests
from api_tests.config_files import config
from api_tests.scripts.apigee_api import ApigeeDebugApi
from assertpy import assert_that

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
                'x-request-id': 'test'
            }
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_consent_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Consent.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_flag_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:Flag.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)

    @pytest.mark.interaction_id
    @pytest.mark.usefixtures('get_token')
    def test_list_put(self):
        # Given
        debug_session = ApigeeDebugApi(config.REASONABLE_ADJUSTMENTS_PROXY)
        expected_interaction_id = 'urn:nhs:names:services:raflags:List.write:1'

        # When
        requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'If-Match': 'abc123'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        actual_interaction_id = debug_session.get_apigee_header('Interaction-ID')

        assert_that(expected_interaction_id).is_equal_to(actual_interaction_id)
