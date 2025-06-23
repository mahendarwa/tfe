workload_pool = workload_identity_config.workload_pool else null

valid_project_name_pattern = "ge[0-9]+-gke-[a-z0-9]+"


if workload_pool == null or not regex.match(valid_project_name_pattern, workload_pool) {
    print("invalid", r.address, "workload_pool does not match new project naming convention, received:", workload_pool)
    violating_clusters += 1
}
