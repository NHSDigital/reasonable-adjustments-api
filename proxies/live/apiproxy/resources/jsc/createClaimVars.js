subClaim = context.setVariable('subClaim', 'https://fhir.nhs.uk/Id/sds-role-profile-id|' + context.getVariable('request.header.nhsd-session-urid'))
requestingSystemClaim = context.setVariable('requestingSystemClaim', 'https://fhir.nhs.uk/Id/accredited-system|' + context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.asid'))
requestingOrganisationClaim = context.setVariable('requestingOrganisationClaim', 'https://fhir.nhs.uk/Id/ods-organization-code|' + context.getVariable('verifyapikey.VerifyAPIKey.CustomAttributes.ods'))
requestingUserClaim = context.setVariable('requestingUserClaim', 'https://fhir.nhs.uk/Id/sds-role-profile-id|' + context.getVariable('request.header.nhsd-session-urid'))
