result := "fail" {
  input.properties.nativeType == "dataflow#job"
  not input.properties.region == allowed_types[_]
}

currentConfiguration := sprintf("Region used: %v", [input.properties.region])
expectedConfiguration := sprintf("Allowed regions: %v", [allowed_types])
