from api_tests.scripts.generic_request import GenericRequest

class CheckReasonableAdjustments(GenericRequest):
    def __init__(self):
        super(CheckReasonableAdjustments, self).__init__()

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
        