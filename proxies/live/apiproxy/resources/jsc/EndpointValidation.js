var requestVerb = context.getVariable('request.verb')
var requestPayload = context.getVariable('request.content')
var internalServerError = false
var invalidResponse = false

var xRequestId = context.getVariable('request.header.X-Request-ID')
var nhsdSessionURID = context.getVariable('request.header.NHSD-Session-URID')
var contentType = context.getVariable('request.header.content-type')
// var asid = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
// var ods = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
print(requestPayload)

var regex = RegExp('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}');

if (!regex.test(xRequestId) || xRequestId === null) {
    var errorDescription = "x-request-id is missing or invalid"
    var invalidResponse = true
}
else if (nhsdSessionURID === "" || nhsdSessionURID === null) {
    var errorDescription = "nhsd-session-urid is missing or invalid"
    var invalidResponse = true
}
else if (requestVerb !== "GET" && contentType !== "application/fhir+json") {
    var errorDescription = "content-type must be set to application/fhir+json"
    var invalidResponse = true
}
else if (requestVerb !== "GET" && requestPayload === "") {
    var errorDescription = "requires payload"
    var invalidResponse = true
}
// else if (asid === null) {
//     var errorDescription = "An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID"
//     var internalServerError = true
// }
// else if (ods === null) {
//     var errorDescription = "An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID"
//     var internalServerError = true
// }

context.setVariable('internalServerError', internalServerError)
context.setVariable('invalidResponse', invalidResponse)

if (internalServerError || invalidResponse) context.setVariable('validation.errorDescription', errorDescription)
