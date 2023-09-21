const ThresholdCodeGet =  {
    method: 'GET',
    path: '/ThresholdCode',
    handler: (request, h) => {
        if (request.query["patient"] != '5900026175') {
            const path = 'ThresholdCodeGETerror.json'
            return h.response(h.file(path)).code(404);
        }
            const path = 'ThresholdCodeGET.json'
            return h.response(h.file(path))
            .header('content-type', 'application/fhir+json')
            .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT');
    }
  };

module.exports = [ThresholdCodeGet]
