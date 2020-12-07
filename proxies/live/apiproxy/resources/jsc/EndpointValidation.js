var requestVerb = context.getVariable('request.verb')
var requestPayload = context.getVariable('request.content')
var isError = false

var xRequestId = context.getVariable('request.header.X-Request-ID')
var nhsdSessionURID = context.getVariable('request.header.NHSD-Session-URID')
var contentType = context.getVariable('request.header.content-type')
var asid = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
var ods = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
var accept = context.getVariable('request.header.accept')
print(requestPayload)

var regex = RegExp('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}');

if (!regex.test(xRequestId) || xRequestId === null) {
    var errorObject = { error: 'invalid header', errorDescription: "x-request-id is missing or invalid", statusCode: 400, reasonPhrase: "Bad Request" } 
    var isError = true
}
else if (nhsdSessionURID === "" || nhsdSessionURID === null) {
    var errorObject = { error: 'invalid header', errorDescription: "nhsd-session-urid is missing or invalid", statusCode: 400, reasonPhrase: "Bad Request" } 
    var isError = true
}
else if (requestVerb !== "GET" && contentType !== "application/json") {
    var errorObject = { error: 'invalid header', errorDescription: "content-type must be set to application/json", statusCode: 400, reasonPhrase: "Bad Request" } 
    var isError = true
}
else if (accept !== "application/fhir+json") {
    var errorObject = { error: 'invalid header', errorDescription: "accept must be set to application/fhir+json", statusCode: 400, reasonPhrase: "Bad Request" } 
    var isError = true
}
else if (requestVerb !== "GET" && requestPayload === "") {
    var errorObject = { error: 'invalid request payload', errorDescription: "requires payload", statusCode: 400, reasonPhrase: "Bad Request" } 
    var isError = true
}
else if (asid === null) {
    var errorObject = { error: 'missing ASID', errorDescription: "An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID", statusCode: 500, reasonPhrase: "Internal Server Errort" } 
    var isError = true
}
else if (ods === null) {
    var errorObject = { error: 'missing ODS', errorDescription: "An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID", statusCode: 500, reasonPhrase: "Internal Server Error" } 
    var isError = true
}

context.setVariable('isError', isError)

if (isError) {
    context.setVariable('validation.errorMessage', errorObject.error)
    context.setVariable('validation.errorDescription', errorObject.errorDescription)
    context.setVariable('validation.statusCode', errorObject.statusCode)
    context.setVariable('validation.reasonPhrase', errorObject.reasonPhrase)    
}
