subClaim = 'https://fhir.nhs.uk/Id/sds-role-profile-id|' + context.getVariable('request.header.nhsd-session-urid')
requestingSystemClaim = 'https://fhir.nhs.uk/Id/accredited-system|' + context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.asid')
requestingOrganisationClaim = 'https://fhir.nhs.uk/Id/ods-organization-code|' + context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.ods')
requestingUserClaim = 'https://fhir.nhs.uk/Id/sds-role-profile-id|' + context.getVariable('request.header.nhsd-session-urid')
scope = context.getVariable('kvm_scope')
audience = 'https://' + context.getVariable('environment.name') + '.api.service.nhs.uk/' + context.getVariable('proxy.basepath')+ context.getVariable('proxy.pathsuffix')

header = {
  "alg": "none",
  "typ": "JWT"
}

payload = {
  sub: subClaim,
  iss: "http://api.service.nhs.uk",
  aud: audience,
  reason_for_request: "directcare",
  scope: scope,
  requesting_organization: requestingOrganisationClaim,
  requesting_system: requestingSystemClaim,
  requesting_user: requestingUserClaim
}

headerB64 =Base64.encode(JSON.stringify(header))
payloadB64 =Base64.encode(JSON.stringify(payload))

context.setVariable("spineJwt", headerB64 + "." + payloadB64 + ".")
