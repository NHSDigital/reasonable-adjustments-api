var parameter = properties.path;
var path = context.getVariable(parameter).substring(1);
context.setVariable("trimmedPath", path);
