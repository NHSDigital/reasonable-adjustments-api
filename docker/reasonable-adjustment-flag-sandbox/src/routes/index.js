const consentEndpoint = require('./consentEndpoint');
const flagEndpont = require('./flagEndpoint');
const underlyingConditionListEndpoint=require('./underlyingConditionListEndpoint');
const ThresholdCodeEndpoint=require('./ThresholdCodeEndpoint');
const listEndpoint = require('./listEndpoint');
const removerarecordEndpoint = require('./removerarecordEndpoint');
const statusEndpoint = require('./statusEndpoint');

const routes = [].concat(consentEndpoint, flagEndpont, listEndpoint, removerarecordEndpoint, statusEndpoint, underlyingConditionListEndpoint, ThresholdCodeEndpoint)

module.exports = routes
