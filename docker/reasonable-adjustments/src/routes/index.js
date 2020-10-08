const consentEndpoint = require('./consentEndpoint');
const flagEndpont = require('./flagEndpoint');
const listEndpoint = require('./listEndpoint');
const removerarecordEndpoint = require('./removerarecordEndpoint');
const statusEndpoint = require('./statusEndpoint');

const routes = [].concat(consentEndpoint, flagEndpont, listEndpoint, removerarecordEndpoint, statusEndpoint)

module.exports = routes
