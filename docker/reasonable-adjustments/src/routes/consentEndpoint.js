const consentGet =  {
    method: 'GET',
    path: '/consent',
    handler: (request, h) => {        
        const path = 'consentGET.json'
        return h.file(path)
    }
  };

const consentPost = {
    method: 'POST',
    path: '/consent',
    handler: (request, h) => {
        const path = 'consentPOST.json'
        return h.response(h.file(path)).code(201);
    }
};

const consentPut = {
    method: 'PUT',
    path: '/consent/{consentID}',
    handler: (request, h) => {
        const path = 'consentPUT.json'
        return h.file(path)
    }
};

module.exports = [consentGet, consentPost, consentPut]
