from api_tests.config_files import config
import pytest
import json
import requests

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}" 

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}" 

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

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

        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"


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
        assert expected_status_code == response.status_code, f"Expected status code: {expected_status_code} Actual: {response.status_code}"

        # assert self.reasonable_adjustments.check_endpoint(
        #     verb='PUT',
        #     endpoint=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
        #     expected_status_code=200,
        #     expected_response=None,
        #     headers={
        #         'Authorization': f'Bearer {self.token}',
        #         'nhsd-session-urid': 'test',
        #         'x-request-id': 'test',
        #         'content-type': 'application/fhir+json',
        #         'if-match': 'test'
        #     },
        #     data=json.dumps({'message': 'test'})
        # )

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_remove_ra_record_get(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='remove_ra_record',
            expected_status_code=200,
            expected_response=None,
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
            data=json.dumps({'message': 'test'})
        )
