import requests
import time
import json

from api_tests.config_files import config
from assertpy import assert_that
import uuid

from api_tests.tests import request_bank
from api_tests.tests.request_bank import Request

def get_details(response):
    result_dict = json.loads(response.text)
    adjustment_id = None
    version_id = None

    if 'total' in result_dict:
        if result_dict['total'] > 0:
            adjustment_id = result_dict['entry'][0]['resource']['id']
            version_id = 'W/"' + result_dict['entry'][0]['resource']['meta']['versionId'] + '"'
    return {'id': adjustment_id, 'version': version_id}


class Utils:
    """ A Utils class to be used for shared functionality between tests  """

    @staticmethod
    def send_request(auth_token: str) -> requests.Response:
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={'patient': 'test', 'category': 'test', 'status': 'test'},
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'x-correlation-id': str(uuid.uuid4())
            }
        )

        return response

    @staticmethod
    def get_etag(auth_token: str, resource_url: str, params):
        response = requests.get(
            url=resource_url,
            params=params,
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
            }
        )

        return response.headers['etag']

    @staticmethod
    def send_consent_post(auth_token: str):
        expected_status_code = 201

        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_CONSENT,
            json=request_bank.get_body(Request.CONSENT_POST),
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            })

        assert_that(expected_status_code).is_equal_to(response.status_code)

        return response

    @staticmethod
    def send_consent_get(auth_token: str):
        response = requests.get(
            url= config.REASONABLE_ADJUSTMENTS_CONSENT,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )

        return get_details(response)

    @staticmethod
    def send_flag_get(auth_token: str):
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'category': 'https://fhir.nhs.uk/STU3/CodeSystem/RARecord-FlagCategory-1|NRAF',
                'status': 'active'
            },
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        )

        return get_details(response)

    @staticmethod
    def send_flag_post(auth_token: str):
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_FLAG,
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            },
            json=request_bank.get_body(Request.FLAG_POST),
        )

        return response

    @staticmethod
    def send_list_get(auth_token:str):
        response = requests.get(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            params={
                'patient': config.TEST_PATIENT_NHS_NUMBER,
                'status': 'active',
                'code': 'http://snomed.info/sct|1094391000000102'
            },
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'Accept': 'application/fhir+json',
            }
        )

        return get_details(response)

    @staticmethod
    def send_list_post(auth_token: str):
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_LIST,
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json'
            },
            json=request_bank.get_body(Request.LIST_POST),
        )

        return response

    @staticmethod
    def send_raremoverecord_post(auth_token: str):
        response = requests.post(
            url=config.REASONABLE_ADJUSTMENTS_REMOVE_RA_RECORD,
            headers={
                'Authorization': f'Bearer {auth_token}',
                'nhsd-session-urid': config.TEST_NHSD_SESSION_URID,
                'x-request-id': str(uuid.uuid4()),
                'content-type': 'application/fhir+json',
                'If-Match': 'W/"1"'
            },
            json=request_bank.get_body(Request.REMOVE_RA_RECORD_POST)
        )

        return response
