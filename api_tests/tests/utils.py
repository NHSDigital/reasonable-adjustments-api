import requests
import pytest
from api_tests.config_files.config import REASONABLE_ADJUSTMENTS_CONSENT

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
                'x-request-id': 'test',
            }
        )

        return response
