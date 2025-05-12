package wiz

default result := "pass"

result := "fail" {
	input.properties.type == "artifactregistry#repository"
	input.properties.hasIAMAccessFromOutsideOrganization
	not input.properties.hasIAMAccessFromExternalSubscription
}

currentConfiguration := {
	"hasIAMAccessFromOutsideOrganization": input.properties.hasIAMAccessFromOutsideOrganization,
	"hasIAMAccessFromExternalSubscription": input.properties.hasIAMAccessFromExternalSubscription
}

expectedConfiguration := {
	"hasIAMAccessFromOutsideOrganization": false,
	"hasIAMAccessFromExternalSubscription": true
}
