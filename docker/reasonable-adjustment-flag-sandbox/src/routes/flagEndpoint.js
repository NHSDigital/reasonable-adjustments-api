const flagGet =  {
    method: 'GET',
    path: '/Flag',
    handler: (request, h) => {
        if (request.query["patient"] != '5900026175') {
            const path = 'flagGETerror.json'
            return h.response(h.file(path)).code(404);
        }
            const path = 'flagGET.json'
            return h.response(h.file(path))
            .header('content-type', 'application/fhir+json')
            .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT');
    }
  };

const flagPost = {
    method: 'POST',
    path: '/Flag',
    handler: (request, h) => {
        const path = 'flagPOST.json'
        return h.response(h.file(path)).code(201)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Location', 'https://clinicals.spineservices.nhs.uk/STU3/Flag/2acb0536-0a8f-48c9-8a2f-6ee82860f186/_history/aa755bd6-2be9-4971-972a-6724879c5cb1')
        .header('Etag', 'W/"aa755bd6-2be9-4971-972a-6724879c5cb1”');
    }
};

const flagPut = {
    method: 'PUT',
    path: '/Flag/{flagID}',
    handler: (request, h) => {
        const path = 'flagPUT.json'
        return h.file(path)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Thur, 25 Jul 2018 11:00:00 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Etag', 'W/"aa755bd6-2be9-4971-972a-6724879c5cb1”');
    }
};

module.exports = [flagGet, flagPost, flagPut]
