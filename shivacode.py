result := "fail" {
	input.properties.type == "artifactregistry#repository"
	count(input.properties.hasIAMAccessFromOutsideOrganization) > 0
	count(input.properties.hasIAMAccessFromExternalSubscription) == 0
}
