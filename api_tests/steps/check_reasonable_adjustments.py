import requests
from api_tests.config_files import config
import json
from urllib.parse import urlparse
import re


class CheckReasonableAdjustments:
    def __init__(self):
        super(CheckReasonableAdjustments, self).__init__()
        self.session = requests.Session()
        self.endpoints = config.ENDPOINTS

    def check_endpoint(self, verb: str, endpoint: str, expected_status_code: int,
                       expected_response: dict or str or list or None, **kwargs) -> bool:
        """Check a given request is returning the expected values. NOTE the expected response can be either a dict,
        a string or a list this is because we can expect either json, html or a list of keys from a json response
        respectively."""
        response = self.get_response(verb, endpoint, **kwargs)

        if type(expected_response) is list:
            return self.verify_response_keys(response, expected_status_code, expected_keys=expected_response)

        if expected_response is None:
            return self.verify_response_content_type(response, expected_status_code)

        # Check response
        return self.verify_response(response, expected_status_code, expected_response=expected_response)

    def get_response(self, verb: str, endpoint: str, **kwargs) -> 'response type':
        """Verify the arguments and then send a request and return the response"""
        try:
            url = self.endpoints[endpoint]
        except KeyError:
            if self.is_url(endpoint):
                url = endpoint
            else:
                raise Exception("Endpoint not found")

        # Verify http verb is valid
        if verb.lower() not in ['post', 'get', 'put']:
            raise Exception(f"Verb: {verb} is invalid")

        func = ((self.get, self.put)[verb.lower() == 'put'], self.post)[verb.lower() == 'post']

        # Get response
        return func(url, **kwargs)

    def get(self, url: str, **kwargs) -> 'response type':
        """Sends a get request and returns the response"""
        try:
            return self.session.get(url, **kwargs)
        except requests.ConnectionError:
            raise Exception(f"the url: {url} does not exist or is invalid")

    def post(self, url: str, **kwargs) -> 'response type':
        """Sends a post request and returns the response"""
        try:
            return self.session.post(url, **kwargs)
        except requests.ConnectionError:
            raise Exception(f"the url: {url} does not exist or is invalid")

    def put(self, url: str, **kwargs) -> 'response type':
        """Sends a put request and returns the response"""
        try:
            return self.session.put(url, **kwargs)
        except requests.ConnectionError:
            raise Exception(f"the url: {url} does not exist or is invalid")

    def verify_response_keys(self, response: 'response type', expected_status_code: int, expected_keys: list) -> bool:
        """Check a given response is returning the correct keys.
        In case the content is dynamic we can only check the keys and not the values"""
        self._validate_response(response)

        data = json.loads(response.text)

        if 'error' in data:
            assert data == expected_keys
        else:
            actual_keys = list(data.keys())
            assert sorted(actual_keys) == sorted(expected_keys), \
                "Expected: {sorted(expected_keys)} but got: {sorted(actual_keys)}"

        assert response.status_code == expected_status_code, f"Status code is incorrect, " \
                                                             f"expected {expected_status_code} " \
                                                             f"but got {response.status_code}"
        return True

    @staticmethod
    def _validate_response(response: 'response type') -> None:
        """Verifies the response provided is of a valid response type"""
        if not type(response) == requests.models.Response:
            raise TypeError("Expected response type object for response argument")

    def verify_response_content_type(self, response: 'response type', expected_status_code: int) -> bool:
        """Check a given response has returned the expected key value pairs"""

        assert self.check_status_code(response, expected_status_code), f"Status code is incorrect, " \
                                                                       f"expected {expected_status_code} " \
                                                                       f"but got {response.status_code}"

        assert self.is_valid_json(response), "Response body is not json or valid json"

        return True

    def check_status_code(self, response: 'response type', expected_status_code: int) -> bool:
        """Compare the actual and expected status code for a given response"""
        self._validate_response(response)
        self._verify_status_code(expected_status_code)
        return response.status_code == expected_status_code

    def is_valid_json(self, response):
        try:
            json.loads(response.text)
        except json.JSONDecodeError:
            return False

        return True

    @staticmethod
    def _verify_status_code(status_code: int or str) -> None:
        """Verifies the status code provided is a valid status code"""
        if not type(status_code) == int:
            try:
                int(status_code)
            except ValueError:
                raise TypeError('Status code must only consist of numbers')
        else:
            if len(str(status_code)) != 3:
                raise TypeError('Status code must be a 3 digit number')

    @staticmethod
    def is_url(url: str) -> bool:
        """Check if a string looks like a URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def verify_response(self, response: 'response type', expected_status_code: int,
                        expected_response: dict or str) -> bool:
        """Check a given response has returned the expected key value pairs"""

        assert self.check_status_code(response, expected_status_code), f"Status code is incorrect, " \
                                                                       f"expected {expected_status_code} " \
                                                                       f"but got {response.status_code}"

        try:
            data = json.loads(response.text)
            # Strip out white spaces
            actual_response = dict(
                (k.strip() if isinstance(k, str) else k,
                 v.strip() if isinstance(v, str) else v
                 ) for k, v in data.items()
            )

            if response.status_code >= 400:
                assert self.error_assertion_has_message_id(actual_response), "Error response missing message_id property"

            actual_response.pop('message_id', None)
            print(actual_response)
            print(expected_response)

            assert actual_response == expected_response, "Actual response is different from the expected response"
        except json.JSONDecodeError:
            # Might be HTML
            # We need to get rid of the dynamic state here so we can compare the text to the stored value
            actual_response = re.sub('<input name="state" type="hidden" value="[a-zA-Z0-9_-]{36}">', '', response.text)

            assert actual_response.replace('\n', '').replace(' ', '').strip() == expected_response.replace('\n', '')\
                .replace(' ', '').strip(), "Actual response is different from the expected response"

        return True

    def error_assertion_has_message_id(self, response) -> bool:
        """Responses with 4xx & 5xx codes should have a message_id property."""
        try:
            a = response['message_id']
            return True
        except KeyError:
            return False
