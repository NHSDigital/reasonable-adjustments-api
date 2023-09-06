import json
import uuid
import pytest
import requests
from assertpy import assert_that

from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request
from api_tests.tests.utils import Utils


@pytest.mark.usefixtures("test_teardown")
class TestHappyCasesSuite:
    """ A test suite to verify all the happy path endpoints """

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_consent_get_without_consent(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        result_dict = json.loads(response.text)
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(result_dict['total']).is_equal_to(0)  # Validate patient record does not contain a consent flag

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_consent_get_with_consent(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={**nhsd_apim_auth_headers,
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
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_consent_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_prefer_response_async(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 202

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Consent",
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Prefer': 'respond-async'
            }
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_consent_put(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 200

        # And
        consent = Utils.send_consent_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        consent_id = consent['id']
        version_id = consent['version']

        print(version_id)

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/Consent/{consent_id}",
            json=request_bank.get_body(Request.CONSENT_PUT),
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-Match': version_id
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_flag_get_without_flag(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Flag",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={**nhsd_apim_auth_headers,
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
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_flag_get_with_flag(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req: Patient record with both a consent and flag
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        Utils.send_flag_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Flag",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={**nhsd_apim_auth_headers,
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
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_flag_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req: Patient has a consent
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/Flag",
            headers={**nhsd_apim_auth_headers,
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
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_flag_put(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req: Patient has both a consent and flag
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        Utils.send_flag_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        get_flag_response = Utils.send_flag_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Given
        expected_status_code = 200
        flag_id = get_flag_response['id']
        version_id = get_flag_response['version']

        print(version_id)

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/Flag/{flag_id}",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
                'if-match': version_id,
            },
            json=request_bank.get_body(Request.FLAG_PUT)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_list_get(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/List",
            params={
                'patient': '9693892283',
                'status': 'active',
                'code': 'http://snomed.info/sct|1094391000000102'
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_list_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req - Patient has consent
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/List",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
                'Prefer': 'return=representation'
            },
            json=request_bank.get_body(Request.LIST_POST)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_list_put(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)
        Utils.send_list_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        get_list_response = Utils.send_list_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers)
        list_id = get_list_response['id']
        version_id = get_list_response['version']

        print(version_id)

        # Given
        expected_status_code = 200
        req_body = request_bank.get_body(Request.LIST_PUT)
        req_body['id'] = list_id

        # When
        response = requests.put(
            url=f"{nhsd_apim_proxy_url}/List/{list_id}",
            headers={**nhsd_apim_auth_headers,
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
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_remove_ra_record_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre_Req : Patient record with a consent
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 200

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/$removerarecord",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'if-Match': 'W/"1"'
            },
            json=request_bank.get_body(Request.REMOVE_RA_RECORD_POST)
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.skip(reason="The ASID we use for testing can not perform this interaction, we have tried adding the interactions on the VEIT07 environment but continue to get the same error")
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_thresholdcode_get(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/ThresholdCode",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        print(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.skip(reason="The ASID we use for testing can not perform this interaction, we have tried adding the interactions on the VEIT07 environment but continue to get the same error")
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_underlyingCondition_get(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/UnderlyingConditionList",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        print(response.text)

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.skip(reason="The ASID we use for testing can not perform this interaction, we have tried adding the interactions on the VEIT07 environment but continue to get the same error")
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_underlyingCondition_post(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Pre-Req: Patient has a consent
        Utils.send_consent_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, test_app_with_attributes)

        # Given
        expected_status_code = 201

        # When
        response = requests.post(
            url=f"{nhsd_apim_proxy_url}/UnderlyingConditionList",
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
            },
            json=request_bank.get_body(Request.UnderlyingConditionList_POST),
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
