const listGet =  {
    method: 'GET',
    path: '/List',
    handler: (request, h) => {
        if (request.query["patient"] != '9693892283') {
            const path = 'listGETerror.json'
            return h.response(h.file(path)).code(404);
        }
        const path = 'listGET.json'
        return h.file(path)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT');
    }
  };

const listPost = {
    method: 'POST',
    path: '/List',
    handler: (request, h) => {
        const path = 'listPOST.json'
        return h.response(h.file(path)).code(201)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Location', 'https://clinicals.spineservices.nhs.uk/STU3/List/130f416a-055d-4a5d-a453-2b7c2de3b57b/_history/f2fef5e5-c38a-408c-a9bc-2d49923928f8')
        .header('Etag', 'W/"f2fef5e5-c38a-408c-a9bc-2d49923928f8”');
    }
};

const listPut = {
    method: 'PUT',
    path: '/List/{listID}',
    handler: (request, h) => {
        const path = 'listPUT.json'
        return h.file(path)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Thur, 25 Jul 2018 11:00:00 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Etag', 'W/"d65be6d8-128a-40f2-9a1d-b250d6485c6d”');
    }
};

module.exports = [listGet, listPost, listPut]
