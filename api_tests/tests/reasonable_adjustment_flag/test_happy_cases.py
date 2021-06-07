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
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
    @pytest.mark.sandbox
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
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
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
        consent = Utils.send_consent_get(self.token)
        consent_id = consent['id']
        version_id = consent['version']

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT + '/' + consent_id,
            json=request_bank.get_body(Request.CONSENT_PUT),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': version_id
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_get_without_flag(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        result_dict = json.loads(response.text)
        assert_that(result_dict['total']).is_equal_to(0)  # Validate patient record does not contain a consent flag

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_get_with_flag(self):
        # Pre-Req: Patient record with both a consent and flag
        Utils.send_consent_post(self.token)
        Utils.send_flag_post(self.token)

        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        result_dict = json.loads(response.text)
        assert_that(result_dict['total']).is_equal_to(1)  # Validate patient record contains a flag

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_post(self):
        # Pre-Req: Patient has a consent
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
            },
            json=request_bank.get_body(Request.FLAG_POST),
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_flag_put(self):
        # Pre-Req: Patient has both a consent and flag
        Utils.send_consent_post(self.token)
        Utils.send_flag_post(self.token)
        get_flag_response = Utils.send_flag_get(self.token)

        # Given
        expected_status_code = 200
        flag_id = get_flag_response['id']
        version_id = get_flag_response['version']

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_FLAG + '/' + flag_id,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
                'If-match': version_id,
            },
            json=request_bank.get_body(Request.FLAG_PUT)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_get(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'status': 'active',
                'code': 'http://snomed.info/sct|1094391000000102'
            },
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_post(self):
        # Pre-Req - Patient has consent
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            },
            json=request_bank.get_body(Request.LIST_POST)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_list_put(self):
        # Pre-Req
        Utils.send_consent_post(self.token)
        Utils.send_list_post(self.token)
        get_list_response = Utils.send_list_get(self.token)
        list_id = get_list_response['id']
        version_id = get_list_response['version']

        # Given
        expected_status_code = 200
        req_body = request_bank.get_body(Request.LIST_PUT)
        req_body['id'] = list_id

        # When
        response = requests.put(
            url=config.REASONABLE_ADJUSTMENTS_LIST + '/' + list_id,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'accept': 'application/fhir+json',
                'if-match': version_id,
            },
            data=json.dumps(req_body)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_remove_ra_record_post(self):
        # Pre_Req : Patient record with a consent
        Utils.send_consent_post(self.token)

        # Given
        expected_status_code = 200

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': 'W/"1"'
            },
            json=request_bank.get_body(Request.REMOVE_RA_RECORD_POST)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_prefer_response_async(self):
        # Given
        expected_status_code = 202

        # When
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Prefer': 'respond-async'
            }
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
