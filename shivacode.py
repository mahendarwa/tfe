package wiz

default result := "pass"

result := "fail" {
	input.properties.type == "artifactregistry#repository"
	input.properties.hasIAMAccessFromOutsideOrganization
	not input.properties.hasIAMAccessFromExternalSubscription
}

currentConfiguration := {
	"type": input.properties.type,
	"hasIAMAccessFromOutsideOrganization": input.properties.hasIAMAccessFromOutsideOrganization,
	"hasIAMAccessFromExternalSubscription": input.properties.hasIAMAccessFromExternalSubscription
}

expectedConfiguration := {
	"type": "artifactregistry#repository",
	"hasIAMAccessFromOutsideOrganization": false,
	"hasIAMAccessFromExternalSubscription": true
}
