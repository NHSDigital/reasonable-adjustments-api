const consentGet =  {
    method: 'GET',
    path: '/Consent',
    handler: (request, h) => {
        if (request.query["patient"] != '5900026175') {
            const path = 'consentGETerror.json'
            return h.response(h.file(path)).code(404);
        }
        const path = 'consentGET.json'
        return h.file(path)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT');
    }
  };

const consentPost = {
    method: 'POST',
    path: '/Consent',
    handler: (request, h) => {
        const path = 'consentPOST.json'
        let response_status_code = 201
        if ('prefer' in request.headers && request.headers['prefer'] === 'respond-async') {
          response_status_code = 202
        }
        return h.response(h.file(path)).code(response_status_code)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Location', 'resourceURL')
        .header('Etag', 'W/"resourceVID”');
    }
};

const consentPut = {
    method: 'PUT',
    path: '/Consent/{consentID}',
    handler: (request, h) => {
        const path = 'consentPUT.json'
        return h.file(path)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Etag', 'W/"resourceVID”');
    }
};

module.exports = [consentGet, consentPost, consentPut]
