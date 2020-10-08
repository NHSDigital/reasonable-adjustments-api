const statusGet =  {
    method: 'GET',
    path: '/_status',
    handler: (request, h) => {        
        const path = 'status.json';
        return h.file(path);
    }
  };

module.exports = [statusGet]
