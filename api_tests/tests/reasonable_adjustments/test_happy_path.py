from api_tests.config_files import config
import pytest
import json

@pytest.mark.usefixtures("setup")
class TestHappyPathSuite:
    """ A test suite to verify all the happy path oauth endpoints """

    @pytest.mark.happy_path
    def test_consent_get(self, use_internal_testing_internal_dev_app, get_token):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
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

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_consent_post(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='consent',
            expected_status_code=201,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_consent_put(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_CONSENT + '/test',
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

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_flag_get(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='flag',
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

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_flag_post(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='flag',
            expected_status_code=201,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_flag_put(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            expected_status_code=200,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_list_get(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='GET',
            endpoint='list',
            expected_status_code=200,
            expected_response=None,
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

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_list_post(self):
        assert self.reasonable_adjustments.check_endpoint(
            verb='POST',
            endpoint='list',
            expected_status_code=201,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json'
            },
            data=json.dumps({'message': 'test'})
        )

    @pytest.mark.happy_path
    @pytest.mark.usefixtures('get_token')
    def test_list_put(self):
        # Test consent endpoint returns a 200 and returns a json response
        assert self.reasonable_adjustments.check_endpoint(
            verb='PUT',
            endpoint=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            expected_status_code=200,
            expected_response=None,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': 'test',
                'content-type': 'application/fhir+json',
                'if-match': 'test'
            },
            data=json.dumps({'message': 'test'})
        )

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
