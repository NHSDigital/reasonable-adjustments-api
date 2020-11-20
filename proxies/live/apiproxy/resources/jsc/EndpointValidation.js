var requestVerb = context.getVariable('request.verb')
var requestPayload = context.getVariable('request.content')
var isError = false

var xRequestId = context.getVariable('request.header.X-Request-ID')
var nhsdSessionURID = context.getVariable('request.header.NHSD-Session-URID')
var contentType = context.getVariable('request.header.content-type')
var asid = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
var ods = context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
print(requestPayload)

var regex = RegExp('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}');
if (!regex.test(xRequestId) || xRequestId === null) {
    var error = "invalid header"
    var errorDescription = "x-request-id is missing or invalid"
    var statusCode = 400
    var reasonPhrase = "Bad Request"
    isError = true
}
else if (nhsdSessionURID === "" || nhsdSessionURID === null) {
    var error = "invalid header"
    var errorDescription = "nhsd-session-urid is missing or invalid"
    var statusCode = 400
    var reasonPhrase = "Bad Request"
    isError = true
}
else if (requestVerb !== "GET" && contentType !== "application/fhir+json") {
    var error = "invalid header"
    var errorDescription = "content-type must be set to application/fhir+json"
    var statusCode = 400
    var reasonPhrase = "Bad Request"
    isError = true
}
else if (requestVerb !== "GET" && requestPayload === "") {
    var error = "invalid request payload"
    var errorDescription = "requires payload"
    var statusCode = 400
    var reasonPhrase = "Bad Request"
    isError = true
}
else if (asid === null) {
    var error = "missing ASID"
    var errorDescription = "An internal server error occurred. Missing ASID. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID"
    var statusCode = 500
    var reasonPhrase = "Internal Server Error"
    isError = true
}
else if (ods === null) {
    var error = "missing ODS"
    var errorDescription = "An internal server error occurred. Missing ODS. Contact us for assistance diagnosing this issue: https://digital.nhs.uk/developer/help-and-support quoting Message ID"
    var statusCode = 500
    var reasonPhrase = "Internal Server Error"
    isError = true
}

context.setVariable('isError', isError)

if (isError) {
    context.setVariable('errorMessage', error)
    context.setVariable('errorDescription', errorDescription)
    context.setVariable('statusCode', statusCode)
    context.setVariable('reasonPhrase', reasonPhrase)    
}
