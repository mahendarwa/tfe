# execute.py

import subprocess
import os

# Teradata credentials from env
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd  = os.getenv("TERADATA_PASSWORD")

# Hardcoded path from update.xml
sql_file_path = "PROC/HSPROCS/sp_OSS_SDO_FHIR_ORG_SDIR_GET.sql"

# Temp file path
temp_file_path = "PROC/HSPROCS/sp_OSS_SDO_FHIR_ORG_SDIR_GET_temp.sql"

# Step 1: Read original file and replace env variable
with open(sql_file_path, "r") as f:
    content = f.read()

# Replace env.id.upper with _DEV
content = content.replace("${env.id.upper}", "_DEV")

# Write to temp file
with open(temp_file_path, "w") as f:
    f.write(content)

# Step 2: BTEQ command to run the SQL
bteq_cmd = f"""
bteq <<EOF
.LOGON {host}/{user},{pwd};
.RUN FILE={temp_file_path};
.LOGOFF;
.QUIT;
EOF
"""

# Step 3: Run the command
subprocess.run(bteq_cmd, shell=True, check=True)
