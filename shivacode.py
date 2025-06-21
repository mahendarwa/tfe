# execute.py

import subprocess
import os
import re

# Teradata credentials from env
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd  = os.getenv("TERADATA_PASSWORD")

# SQL path — your path from repo
sql_file_path = "Teradata/src/PROC/HSPROCS/sp_OSS_SDO_FHIR_ORG_SDIR_GET.sql"
temp_file_path = "Teradata/src/PROC/HSPROCS/sp_OSS_SDO_FHIR_ORG_SDIR_GET_temp.sql"

# Step 1: Read and process .sql
with open(sql_file_path, "r") as f:
    content = f.read()

# Step 2: Remove Liquibase header
# Remove everything before first */
content = re.sub(r'^.*?\*/', '', content, flags=re.DOTALL)

# Step 3: Replace env variable
content = content.replace("${env.id.upper}", "_DEV")

# Step 4: Remove DELIMITER line
content = re.sub(r'^.*SET DELIMITER.*$', '', content, flags=re.MULTILINE)

# Step 5: Replace $$ with ;
content = content.replace('$$', ';')

# Step 6: Save temp file
with open(temp_file_path, "w") as f:
    f.write(content)

# Step 7: BTEQ command
bteq_cmd = f"""
bteq <<EOF
.LOGON {host}/{user},{pwd};
.RUN FILE={temp_file_path};
.LOGOFF;
.QUIT;
EOF
"""

# Step 8: Run BTEQ
subprocess.run(bteq_cmd, shell=True, check=True)
