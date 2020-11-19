const listGet =  {
    method: 'GET',
    path: '/List',
    handler: (request, h) => {
        const path = 'listGET.json'
        return h.file(path)
    }
  };

const listPost = {
    method: 'POST',
    path: '/List',
    handler: (request, h) => {
        const path = 'listPOST.json'
        return h.response(h.file(path)).code(201);
    }
};

const listPut = {
    method: 'PUT',
    path: '/List/{listID}',
    handler: (request, h) => {
        const path = 'listPUT.json'
        return h.file(path)
    }
};

module.exports = [listGet, listPost, listPut]
