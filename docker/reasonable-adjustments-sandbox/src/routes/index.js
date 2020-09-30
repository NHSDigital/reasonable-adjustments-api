const consentEndpoint = require('./consentEndpoint');
const flagEndpont = require('./flagEndpoint');
const listEndpoint = require('./listEndpoint');
const removerarecordEndpoint = require('./removerarecordEndpoint');

//const getStatus = require('./getStatus')

const routes = [].concat(consentEndpoint, flagEndpont, listEndpoint, removerarecordEndpoint)

module.exports = routes
