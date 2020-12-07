import requests
import time

from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_CONSENT
import uuid

class Utils:
    """ A Utils class to be used for shared functionality between tests  """

    @staticmethod
    def send_request(self) -> requests.Response:
        response = requests.get(
            url=REASONABLE_ADJUSTMENTS_CONSENT,
            params={'patient': 'test', 'category': 'test', 'status': 'test'},
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': 'test',
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )

        return response

    @staticmethod
    def get_etag(self, resource_url: str, params):
        response = requests.get(
            url=resource_url,
            params=params,
            headers={
                'Authorization': f'Bearer {self.token}',
                'nhsd-session-urid': str(uuid.uuid4()),
                'x-request-id': str(uuid.uuid4()),
                'Accept': 'application/fhir+json'
            }
        )
        time.sleep(1)

        return response.headers['Etag']
