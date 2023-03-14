const consentEndpoint = require('./consentEndpoint');
const flagEndpont = require('./flagEndpoint');
const underlyingConditionListEndpoint=require('./underlyingConditionListEndpoint');
const listEndpoint = require('./listEndpoint');
const removerarecordEndpoint = require('./removerarecordEndpoint');
const statusEndpoint = require('./statusEndpoint');

const routes = [].concat(consentEndpoint, flagEndpont, listEndpoint, removerarecordEndpoint, statusEndpoint, underlyingConditionListEndpoint)

module.exports = routes
