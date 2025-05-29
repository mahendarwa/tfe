result := "fail" {
  input.properties.nativeType == "dataflow#job"
  not input.properties.region in allowed_types
}
