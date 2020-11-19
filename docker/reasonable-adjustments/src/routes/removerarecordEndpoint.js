const removerarecordPost = {
    method: 'POST',
    path: '/$removerarecord',
    handler: (request, h) => {
        const path = 'removerarecordPOST.json'
        return h.file(path)
    }
};

module.exports = [removerarecordPost]
