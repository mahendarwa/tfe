import os
import re
import xml.etree.ElementTree as ET
import subprocess

# Get execution environment
executionenv = os.getenv("ENV_ID", "")
env_id = f"_{executionenv}" if executionenv.upper() in ('DEV2', 'DEV', 'INT', 'QA', 'UAT') else ""

# Teradata credentials
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

if not all([host, user, pwd]):
    print("❌ Missing TERADATA environment variables")
    exit(1)

# Paths
base_path = "Teradata/src"
update_xml_path = os.path.join(base_path, "update.xml")

# Parse update.xml
tree = ET.parse(update_xml_path)
root = tree.getroot()
ns = {"db": "http://www.liquibase.org/xml/ns/dbchangelog"}
sql_files = [elem.attrib["file"] for elem in root.findall("db:include", ns)]

if not sql_files:
    print("⚠️  No SQL files found in update.xml")
    exit(0)

print("📂 SQL files to execute:")
for file in sql_files:
    print(f"  • {file}")

# Process and execute each SQL file
for sql_file in sql_files:
    full_path = os.path.join(base_path, sql_file)
    if not os.path.exists(full_path):
        print(f"⚠️  Skipping missing SQL file: {full_path}")
        continue

    with open(full_path, "r") as f:
        content = f.read()
        final_sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), content)

    temp_file = "temp_script.sql"
    with open(temp_file, "w") as f:
        f.write(final_sql + "\n")

    # Prepare BTEQ wrapper
    if executionenv.upper() == "UAT":
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},RpSQC\\$c_4dwv;
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
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)

    print("📤 BTEQ Output:\n", result.stdout)
    if result.returncode != 0:
        print(f"❌ Execution failed for {sql_file}:\n", result.stderr)
        exit(result.returncode)

print("\n✅ All SQL files executed successfully.")
