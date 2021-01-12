import json
import uuid

import pytest
import requests
from assertpy import assert_that
from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request

from api_tests.config_files import config
from api_tests.tests.utils import Utils


@pytest.mark.usefixtures("setup")
class TestHappyCasesSuite:
    """ A test suite to verify all the happy path endpoints """

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_get_without_consent(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient': '9692247317',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        result_dict = json.loads(response.text)
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(result_dict['total']).is_equal_to(0) # Validate patient record does not contain a consent flag

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_get_with_consent(self):
        # Pre-Req
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient': '9692247317',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        result_dict = json.loads(response.text)
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(result_dict['total']).is_equal_to(1)  # Validate patient record contains a consent flag

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_post(self):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': '093895563513',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_consent_put(self):
        # Pre-Req
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 200

        # And
        consent = Utils.send_get_consent(self.token)
        consent_id = consent['consent_id']
        version_id = consent['version_id']

        # todo on sandbox the consent_id and version_id cannot be None, need a cleaner way to do this
        if self.sandbox is True:
            consent_id = '1'
            version_id = 'W/"1"'

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT + '/' + consent_id,
            json=request_bank.get_body(Request.CONSENT_PUT),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': '093895563513',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': version_id
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_get(self):

        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            params={
                'patient': '9999999998',
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
    @pytest.mark.sandbox
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
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_put(self):
        # Given
        expected_status_code = 200
        etag = Utils.get_etag(self,
                              config.REASONABLE_ADJUSTMENTS_CONSENT,
                              params={
                                  'patient': '9999999998',
                                  'category': 'test',
                                  'status': 'test',
                              })

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-match': etag,
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_get(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            params={
                'patient': '9999999998',
                'status': 'active',
                'code': 'http://snomed.info/sct|1094391000000102'
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
    @pytest.mark.sandbox
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
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_put(self):
        # Given
        expected_status_code = 200
        etag = Utils.get_etag(self,
                              config.REASONABLE_ADJUSTMENTS_CONSENT,
                              params={
                                  'patient': '9999999998',
                                  'category': 'test',
                                  'status': 'test',
                              })

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/1',
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-match': etag,
            },
            data=json.dumps({'message': 'test'})
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_remove_ra_record_post(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': '093895563513',
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': 'W/"1"'
            },
            json=request_bank.get_body(Request.REMOVE_RA_RECORD_POST)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

