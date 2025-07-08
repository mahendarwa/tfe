package wiz

default result := "fail"

result := "pass" {
  input.maintenancePolicy.window.recurringWindow.window.startTime
  input.maintenancePolicy.window.recurringWindow.window.endTime
}

result := "pass" {
  input.maintenancePolicy.window.dailyMaintenanceWindow.startTime
  input.maintenancePolicy.window.dailyMaintenanceWindow.duration
}

currentConfiguration := sprintf("recurringWindow: %v, dailyMaintenanceWindow: %v", [
  input.maintenancePolicy.window.recurringWindow,
  input.maintenancePolicy.window.dailyMaintenanceWindow
])

expectedConfiguration := "Either recurringWindow (with startTime and endTime) OR dailyMaintenanceWindow (with startTime and duration) should be set"
