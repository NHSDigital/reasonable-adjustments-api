const underlyingConditionListGet =  {
    method: 'GET',
    path: '/UnderlyingConditionList',
    handler: (request, h) => {
        if (request.query["patient"] != '5900026175') {
            const path = 'underlyingConditionListGETerror.json'
            return h.response(h.file(path)).code(404);
        }
            const path = 'underlyingConditionListGET.json'
            return h.response(h.file(path))
            .header('content-type', 'application/fhir+json')
            .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT');
    }
  };

const underlyingConditionListPost = {
    method: 'POST',
    path: '/UnderlyingConditionList',
    handler: (request, h) => {
        const path = 'underlyingConditionListPOST.json'
        return h.response(h.file(path)).code(201)
        .header('content-type', 'application/fhir+json')
        .header('Date', 'Tue, 24 Jul 2018 11:00:01 GMT')
        .header('Last-Modified', '2018-07-24T10:01:00+00:00')
        .header('Location', 'https://clinicals.spineservices.nhs.uk/STU3/underlyingConditionList/2acb0536-0a8f-48c9-8a2f-6ee82860f186/_history/aa755bd6-2be9-4971-972a-6724879c5cb1')
        .header('Etag', 'W/"aa755bd6-2be9-4971-972a-6724879c5cb1”');
    }
};

module.exports = [underlyingConditionListGet, underlyingConditionListPost]
