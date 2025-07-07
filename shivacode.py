package wiz

default result := "pass"

result := "fail" {
  not input.maintenancePolicy.window.recurringWindow
}
result := "fail" {
  not input.maintenancePolicy.window.recurringWindow.window.startTime
}
result := "fail" {
  not input.maintenancePolicy.window.recurringWindow.window.endTime
}
currentConfiguration := sprintf("recurringWindow: %v", [input.maintenancePolicy.window.recurringWindow])
expectedConfiguration := "recurringWindow with startTime and endTime should be set"
