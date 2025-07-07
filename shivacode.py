package gke.maintenance

default compliant = false

compliant {
    input.maintenancePolicy.window.dailyMaintenanceWindow.startTime
    input.maintenancePolicy.window.dailyMaintenanceWindow.duration
}
