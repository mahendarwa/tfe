import os
import re
import xml.etree.ElementTree as ET
import subprocess
import uuid

# Get execution environment
executionenv = os.getenv("ENV_ID", "")
env_id = f"_{executionenv}" if executionenv.upper() in ("DEV2", "DEV", "INT", "QA", "UAT") else ""

# Teradata credentials
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd  = os.getenv("TERADATA_PASSWORD")

if not all([host, user, pwd]):
    print("❌ Missing TERADATA environment variables")
    exit(1)

# Paths
base_path = "Teradata/src"
update_xml_path = os.path.join(base_path, "update.xml")

# Parse update.xml if exists
if not os.path.exists(update_xml_path):
    print(f"⚠️ Skipping XML parse — update.xml not found at: {update_xml_path}")
    exit(0)

tree = ET.parse(update_xml_path)
root = tree.getroot()
ns = {"db": "http://www.liquibase.org/xml/ns/dbchangelog"}
sql_files = [elem.attrib["file"] for elem in root.findall("db:include", ns)]

if not sql_files:
    print("⚠️ No SQL files found in update.xml")
    exit(0)

# Process only PROC/HSPROCS files
printed = set()
valid_proc_files = []

for sql_file in sql_files:
    if not sql_file.startswith("PROC/HSPROCS/"):
        continue
    if sql_file in printed:
        continue
    printed.add(sql_file)
    full_path = os.path.join(base_path, sql_file)
    if os.path.exists(full_path):
        print(f"✅ {full_path}")
        valid_proc_files.append(full_path)
    else:
        print(f"❌ Missing: {full_path}")

# Run BTEQ for each valid PROC file using COMPILE FILE
for proc_file in valid_proc_files:
    with open(proc_file, "r") as f:
        content = f.read()

    content = content.replace("${env.id.upper}", env_id.upper())

    # Prepare temp files
    temp_proc_path = f"{base_path}/{uuid.uuid4()}_proc.sql"
    temp_btq_path  = f"{base_path}/{uuid.uuid4()}_proc.btq"
    log_path       = f"{temp_btq_path}.log"

    # Write PROC to temp file
    with open(temp_proc_path, "w") as f:
        f.write(content)

    # Build BTEQ content
    if executionenv.upper() == "UAT":
        bteq_content = f"""
.LOGON {host}/{user},RpSQC\\\\$c_4dwv;
COMPILE FILE = {temp_proc_path};
.LOGOFF;
.QUIT;
"""
    elif executionenv.upper() == "PRD":
        bteq_content = f"""
.LOGON {host}/{user},\\$_bdgE7r1#Tr;
COMPILE FILE = {temp_proc_path};
.LOGOFF;
.QUIT;
"""
    else:
        bteq_content = f"""
.LOGON {host}/{user},{pwd};
COMPILE FILE = {temp_proc_path};
.LOGOFF;
.QUIT;
"""

    # Save BTEQ script
    with open(temp_btq_path, "w") as f:
        f.write(bteq_content)

    # Run BTEQ
    run_cmd = f"bteq < {temp_btq_path} > {log_path}"
    print(f"\n🚀 Executing PROC file: {proc_file}")
    print(f"Running: {run_cmd}")

    result = subprocess.run(run_cmd, shell=True, check=False)
    if result.returncode != 0:
        print(f"❌ Failed executing {proc_file}. Check log: {log_path}")
        exit(result.returncode)
    else:
        print(f"✅ Completed. See log: {log_path}")

# ✅ Delete update.xml at the end
try:
    os.remove(update_xml_path)
    print(f"\n🗑️ Deleted update.xml after processing: {update_xml_path}")
except Exception as e:
    print(f"❌ Failed to delete update.xml: {e}")
    exit(1)
