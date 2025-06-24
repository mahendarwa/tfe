# execute_proc.py

import subprocess
import os
import uuid

# Teradata credentials from env
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd  = os.getenv("TERADATA_PASSWORD")

# Paths
proc_file_path = "Teradata/src/PROC/HSPROCS/sp_MY_PROC.sql"
temp_proc_path = f"Teradata/src/PROC/HSPROCS/{uuid.uuid4()}_proc.sql"
temp_btq_path  = f"Teradata/src/PROC/HSPROCS/{uuid.uuid4()}_proc.btq"

# Step 1: Read PROC SQL file and process
with open(proc_file_path, "r") as f:
    content = f.read()

# Optional replace env variables (if needed)
content = content.replace("${env.id.upper}", "_DEV")

# Step 2: Write temp PROC file
with open(temp_proc_path, "w") as f:
    f.write(content)

# Step 3: Build BTEQ command to COMPILE PROC
bteq_cmd = f"""
bteq <<EOF
.LOGON {host}/{user},{pwd};
COMPILE FILE = {temp_proc_path};
.LOGOFF;
.QUIT;
EOF
"""

# Step 4: Save .btq file
with open(temp_btq_path, "w") as f:
    f.write(bteq_cmd)

# Step 5: Run BTEQ to deploy PROC
run_cmd = f"bteq < {temp_btq_path} > {temp_btq_path}.log"

print(f"Running: {run_cmd}")

subprocess.run(run_cmd, shell=True, check=True)
