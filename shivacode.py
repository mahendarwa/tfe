import os
import re
import xml.etree.ElementTree as ET
import subprocess

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

# Track printed files to avoid duplicates
printed = set()
valid_files = []

# Print and collect valid non-proc files
for sql_file in sql_files:
    if sql_file.startswith("PROC/HSPROCS/"):
        continue
    if sql_file in printed:
        continue
    printed.add(sql_file)
    full_path = os.path.join(base_path, sql_file)
    if os.path.exists(full_path):
        print(f"✅ {full_path}")
        valid_files.append(full_path)
    else:
        print(f"❌ Missing: {full_path}")

# 🔁 Process and execute each valid SQL file
for sql_file in valid_files:
    with open(sql_file, "r") as f:
        content = f.read()
        final_sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), content)

    temp_file = "temp_script.sql"
    with open(temp_file, "w") as f:
        f.write(final_sql + "\n")

    # BTEQ logic based on environment
    if executionenv.upper() == "UAT":
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},RpSQC\\\\$c_4dwv;
.run file={temp_file};
.logoff;
.quit;
EOF
"""
    elif executionenv.upper() == "PRD":
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},\\$_bdgE7r1#Tr;
.run file={temp_file};
.logoff;
.quit;
EOF
"""
    else:
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},{pwd};
.run file={temp_file};
.logoff;
.quit;
EOF
"""

    print(f"\n🚀 Executing: {sql_file}")
    result = subprocess.run(bteq_cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    print("📤 BTEQ Output:\n", result.stdout)
    if result.returncode != 0:
        print(f"❌ Execution failed for {sql_file}:\n", result.stderr)
        exit(result.returncode)

print("\n✅ All SQL files executed successfully.")

# ✅ Delete update.xml after everything
try:
    os.remove(update_xml_path)
    print(f"\n🗑️ Deleted update.xml after processing: {update_xml_path}")
except Exception as e:
    print(f"❌ Failed to delete update.xml: {e}")
    exit(1)
