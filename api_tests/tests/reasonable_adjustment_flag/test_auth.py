import pytest
import requests
import uuid
from assertpy import assert_that


class TestAuthCasesSuite:
    """ A test suite to verify all the happy path oauth endpoints """

    existing_patient = '5900008142'

    @pytest.mark.integration
    @pytest.mark.nhsd_apim_authorization(
        {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": "ra-test-user"},
        },
        # Allow app-restricted access
        {
            "access": "application",
            "level": "level3",
        }
    )
    def test_asid_auth(self, test_app_with_attributes, nhsd_apim_proxy_url, nhsd_apim_auth_headers):
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{nhsd_apim_proxy_url}/Consent",
            params={
                'patient': self.existing_patient,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={**nhsd_apim_auth_headers,
                'x-request-id': str(uuid.uuid4()),
                'accept': 'application/fhir+json'}
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

