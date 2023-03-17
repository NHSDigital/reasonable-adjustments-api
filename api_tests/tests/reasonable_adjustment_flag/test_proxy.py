import base64
import json
import uuid

import pytest
import requests
from assertpy import assert_that
from pytest_nhsd_apim.apigee_apis import ApigeeNonProdCredentials, ApigeeClient, DeveloperAppsAPI, DebugSessionsAPI
from api_tests.tests.utils import Utils


class TestProxyCasesSuite:
    """ A test suite to verify all the happy path oauth endpoints """

    @pytest.mark.spine_headers
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_ASID_fetch(self, test_app_with_attributes, trace, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        trace.get_debugsessions()
        trace.post_debugsession(session="my_session")
        expected_value = '200000001390'

        # When
        Utils.send_request(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Then
        transaction_ids = trace.get_transaction_data(session_name="my_session")
        data = trace.get_transaction_data_by_id(session_name="my_session", transaction_id=transaction_ids[0])
        actual_asid = trace.get_apigee_variable_from_trace(
            name="app.asid",
            data=data,
        )

        trace.delete_debugsession_by_name(session_name="my_session")

        assert_that(expected_value).is_equal_to(actual_asid)

        actual_header_value = trace.get_apigee_variable_from_trace(
            name="message.header.NHSD-ASID",
            data=data,
        )
        assert_that(expected_value).is_equal_to(actual_header_value)

    @pytest.mark.spine_headers
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_x_request_id_equals_nhsd_request_id(self, test_app_with_attributes, trace, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        trace.post_debugsession(session="my_session")

        # When
        Utils.send_request(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Then
        transaction_ids = trace.get_transaction_data(session_name="my_session")
        data = trace.get_transaction_data_by_id(session_name="my_session", transaction_id=transaction_ids[0])
        trace_id = trace.get_apigee_variable_from_trace(
            name="message.header.NHSD-Request-ID",
            data=data,
        )
        x_request_id = trace.get_apigee_variable_from_trace(
            name="message.header.X-Request-ID",
            data=data,
        )

        trace.delete_debugsession_by_name(session_name="my_session")

        assert_that(trace_id).is_equal_to(x_request_id)

    @pytest.mark.spine_headers
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_outgoing_request_contains_nhsd_correlation_id_header(self, test_app_with_attributes, trace, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        trace.post_debugsession(session="my_session")

        # When
        Utils.send_request(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Then
        transaction_ids = trace.get_transaction_data(session_name="my_session")
        data = trace.get_transaction_data_by_id(session_name="my_session", transaction_id=transaction_ids[0])
        apigee_message_id = trace.get_apigee_variable_from_trace(
            name="messageid",
            data=data,
        )
        x_correlation_id_header = trace.get_apigee_variable_from_trace(
            name="message.header.X-Correlation-ID",
            data=data,
        )
        x_request_id_header = trace.get_apigee_variable_from_trace(
            name="message.header.X-Request-ID",
            data=data,
        )
        nhsd_correlation_id_header = trace.get_apigee_variable_from_trace(
            name="message.header.NHSD-Correlation-ID",
            data=data,
        )

        expected_correlation_id_header = x_request_id_header + '.' + x_correlation_id_header + '.' + apigee_message_id

        trace.delete_debugsession_by_name(session_name="my_session")

        assert_that(expected_correlation_id_header).is_equal_to(nhsd_correlation_id_header)

    @pytest.mark.ods
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_valid_ods(self, test_app_with_attributes, trace, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        trace.post_debugsession(session="my_session")
        expected_ods = 'D82106'

        # When
        Utils.send_request(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Then
        transaction_ids = trace.get_transaction_data(session_name="my_session")
        data = trace.get_transaction_data_by_id(session_name="my_session", transaction_id=transaction_ids[0])
        actual_ods = trace.get_apigee_variable_from_trace(
            name="verifyapikey.VerifyAPIKey.CustomAttributes.ods",
            data=data,
        )

        trace.delete_debugsession_by_name(session_name="my_session")

        assert_that(expected_ods).is_equal_to(actual_ods)

    @pytest.mark.jwt
    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_jwt(self, test_app_with_attributes, trace, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        trace.post_debugsession(session="my_session")
        expected_jwt_claims = {
            'reason_for_request': 'directcare',
            'scope': 'user/Consent.read',
            'requesting_organization': 'https://fhir.nhs.uk/Id/ods-organization-code|D82106',
            'requesting_system': 'https://fhir.nhs.uk/Id/accredited-system|200000001390',
            'requesting_user': f'https://fhir.nhs.uk/Id/sds-role-profile-id|555254242103',
            'sub': f'https://fhir.nhs.uk/Id/sds-role-profile-id|555254242103',
            'iss': 'http://api.service.nhs.uk',
            'aud': f'/{nhsd_apim_proxy_url}/Consent'
        }

        # When
        Utils.send_request(nhsd_apim_proxy_url, nhsd_apim_auth_headers)

        # Then
        transaction_ids = trace.get_transaction_data(session_name="my_session")
        data = trace.get_transaction_data_by_id(session_name="my_session", transaction_id=transaction_ids[0])
        # We should pull Authorization header instead but Apigee mask that value, so we get spineJwt variable instead
        actual_jwt = trace.get_apigee_variable_from_trace(
            name="spineJwt",
            data=data,
        )

        # We manually decode jwt because, jwt library requires all three segments but we only have two (no signature).
        jwt_segments = actual_jwt.split('.')
        actual_jwt_claims = json.loads(base64.b64decode(jwt_segments[1]))

        trace.delete_debugsession_by_name(session_name="my_session")

        assert_that(expected_jwt_claims['reason_for_request']).is_equal_to_ignoring_case(actual_jwt_claims['reason_for_request'])
        assert_that(expected_jwt_claims['scope']).is_equal_to_ignoring_case(actual_jwt_claims['scope'])
        assert_that(expected_jwt_claims['requesting_organization']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_organization'])
        assert_that(expected_jwt_claims['requesting_system']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_system'])
        assert_that(expected_jwt_claims['requesting_user']).is_equal_to_ignoring_case(actual_jwt_claims['requesting_user'])
        assert_that(expected_jwt_claims['sub']).is_equal_to_ignoring_case(actual_jwt_claims['sub'])
        assert_that(expected_jwt_claims['iss']).is_equal_to_ignoring_case(actual_jwt_claims['iss'])
        assert_that(expected_jwt_claims['aud']).is_equal_to_ignoring_case(actual_jwt_claims['aud'])

    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        }
    )
    def test_response_contains_request_id_and_correlation_id_headers(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        # Given
        request_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': '9693892283',
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active',
                '_from': 'json'
            },
            headers={
                **nhsd_apim_auth_headers,
                'x-request-id': request_id,
                'x-correlation-id': correlation_id,
                'Accept': 'application/fhir+json'
            }
        )

        # Then
        assert_that(200).is_equal_to(response.status_code)
        assert_that(response.headers).contains_key('x-request-id')
        assert_that(request_id).is_equal_to(response.headers['x-request-id'])
        assert_that(response.headers).contains_key('x-correlation-id')
        assert_that(correlation_id).is_equal_to(response.headers['x-correlation-id'])

    @pytest.mark.happy_path
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_status_get(self, nhsd_apim_proxy_url, status_endpoint_auth_headers):
        # Given
        expected_status_code = 200
        # When
        response = requests.get(
            f"{nhsd_apim_proxy_url}/_status",
            headers=status_endpoint_auth_headers
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.integration
    def test_ping(self, nhsd_apim_proxy_url):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(f"{nhsd_apim_proxy_url}/_ping")

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
