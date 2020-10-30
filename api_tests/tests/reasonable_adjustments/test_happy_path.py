from api_tests.config_files import config
import pytest
import json
import requests
from assertpy import assert_that

@pytest.mark.usefixtures("setup")
class TestHappyPathSuite:
    """ A test suite to verify all the happy path oauth endpoints """

    @pytest.mark.happy_path
    def test_consent_get(self, use_internal_testing_internal_dev_app, get_token):
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
                'x-request-id': 'test'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
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
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
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
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
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
                'x-request-id': 'test'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_flag_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            json=json.dumps({'message': 'test'})            
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_flag_put(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
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
                'x-request-id': 'test'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_list_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            json=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)


    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_list_put(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
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
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
            },
            json=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
