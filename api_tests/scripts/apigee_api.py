from api_tests.config_files.config import APIGEE_API_URL, APIGEE_AUTHENTICATION, APIGEE_ENVIRONMENT, APIGEE_USERNAME, \
    APIGEE_PASSWORD
import json
import uuid
import base64
import requests


class ApigeeDebugApi:
    def __init__(self, proxy: str):
        super(ApigeeDebugApi, self).__init__()
        self.session = requests.Session()
        self.session_name = self._generate_uuid()
        self.proxy = proxy

        if APIGEE_USERNAME != '' and APIGEE_PASSWORD != '':
            token = base64.b64encode(f'{APIGEE_USERNAME}:{APIGEE_PASSWORD}'.encode('ascii'))
            self.headers = {'Authorization': f'Basic {token.decode("ascii")}'}
        elif APIGEE_AUTHENTICATION != '':
            self.headers = {'Authorization': f'Bearer {APIGEE_AUTHENTICATION}'}
        else:
            raise Exception("None of apigee authentication methods is provided. If you're running this remotely you \
                must provide APIGEE_AUTHENTICATION otherwise provide APIGEE_USERNAME and APIGEE_PASSWORD")

        self.revision = self._get_latest_revision()
        self.create_debug_session()

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

    def check_status_code(self, response: 'response type', expected_status_code: int) -> bool:
        """Compare the actual and expected status code for a given response"""
        self._validate_response(response)
        self._verify_status_code(expected_status_code)
        return response.status_code == expected_status_code

    @staticmethod
    def _validate_response(response: 'response type') -> None:
        """Verifies the response provided is of a valid response type"""
        if not type(response) == requests.models.Response:
            raise TypeError("Expected response type object for response argument")

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
    def _generate_uuid():
        unique_id = uuid.uuid4()
        return str(unique_id)

    def _get_latest_revision(self) -> str:
        url = f"{APIGEE_API_URL}/apis/{self.proxy}/revisions"

        response = self.get(url, headers=self.headers)
        revisions = response.json()
        return revisions[-1]

    def create_debug_session(self):
        url = f"{APIGEE_API_URL}/environments/{APIGEE_ENVIRONMENT}/apis/{self.proxy}/revisions/{self.revision}/" \
              f"debugsessions?session={self.session_name}"

        response = self.post(url, headers=self.headers)

        assert self.check_status_code(response, 201), f"Unable to create apigee debug session {self.session_name}"

    def _get_transaction_id(self) -> str:
        url = f"{APIGEE_API_URL}/environments/{APIGEE_ENVIRONMENT}/apis/{self.proxy}/revisions/{self.revision}/" \
              f"debugsessions/{self.session_name}/data"

        response = self.get(url, headers=self.headers)
        assert self.check_status_code(response, 200), f"Unable to get apigee transaction id for {self.session_name}"
        return response.text.strip('[]').replace("\"", "").strip().split(', ')[0]

    def _get_transaction_data(self) -> dict:
        transaction_id = self._get_transaction_id()
        url = f"{APIGEE_API_URL}/environments/{APIGEE_ENVIRONMENT}/apis/{self.proxy}/revisions/{self.revision}/" \
              f"debugsessions/{self.session_name}/data/{transaction_id}"

        response = self.get(url, headers=self.headers)
        assert self.check_status_code(response, 200), f"Unable to get apigee transaction {transaction_id}"

        return json.loads(response.text)

    def get_apigee_variable(self, name: str) -> str:
        data = self._get_transaction_data()
        executions = [x.get('results', None) for x in data['point'] if x.get('id', "") == "Execution"]
        executions = list(filter(lambda x: x != [], executions))

        variable_accesses = []

        for execution in executions:
            for item in execution:
                if item.get('ActionResult', '') == 'VariableAccess':
                    variable_accesses.append(item)

        for result in variable_accesses:  # Configured by the application
            for item in result['accessList']:
                if item.get('Get', {}).get('name', '') == name:
                    return item.get('Get', {}).get('value', '')

    def get_apigee_header(self, name: str) -> str:
        data = self._get_transaction_data()
        executions = [x.get('results', None) for x in data['point'] if x.get('id', "") == "Execution"]
        executions = list(filter(lambda x: x != [], executions))

        request_messages = []

        for execution in executions:
            for item in execution:
                if item.get('ActionResult', '') == 'RequestMessage':
                    request_messages.append(item)

        for result in request_messages:  # One being sent as the header
            for item in result['headers']:
                if item['name'] == name:
                    return item['value']
