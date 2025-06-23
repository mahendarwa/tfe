valid_new_pattern = "ge[0-9]+-gke-[a-z0-9]+"
if (workload_pool == null) or 
   (not workload_pool contains "prj" and not regex.match(valid_new_pattern, workload_pool)) { ... }
