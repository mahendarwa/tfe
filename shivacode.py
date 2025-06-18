import os
import re
import xml.etree.ElementTree as ET
import subprocess
import glob

# Get execution environment
executionenv = os.getenv("ENV_ID", "")
env_id = f"_{executionenv}" if executionenv.upper() in ('DEV2', 'DEV', 'INT', 'QA') else ""

# Teradata credentials
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

if not all([host, user, pwd]):
    print("❌ Missing TERADATA environment variables")
    exit(1)

# Cleanup duplicate update.xml
base_path = "Teradata/src"
for xml_file in glob.glob("**/update*.xml", recursive=True):
    if not xml_file.endswith("Teradata/src/update.xml"):
        print(f"🗑️ Removing outdated update file: {xml_file}")
        os.remove(xml_file)

# Parse update.xml
update_xml_path = os.path.join(base_path, "update.xml")
tree = ET.parse(update_xml_path)
root = tree.getroot()
ns = {"db": "http://www.liquibase.org/xml/ns/dbchangelog"}
sql_files = [elem.attrib["file"] for elem in root.findall("db:include", ns)]

if not sql_files:
    print("⚠️ No SQL files found in update.xml")
    exit(0)

print("📂 SQL files to execute/deploy:")
for file in sql_files:
    print(f"  * {file}")

# Process each file
for sql_file in sql_files:
    full_path = os.path.join(base_path, sql_file)

    if not os.path.exists(full_path):
        print(f"⚠️ Skipping missing SQL file: {full_path}")
        continue

    with open(full_path, "r") as f:
        content = f.read()
        final_sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), content)

    is_proc = sql_file.startswith("PROC/HSPROCS/")

    if is_proc:
        print(f"\n🚀 Deploying PROCEDURE file: {sql_file}")

        # Strip liquibase comments (robust)
        proc_body = []
        skip = False
        for line in final_sql.splitlines():
            if line.strip().startswith('--liquibase'):
                continue
            if line.strip().startswith('--changeset'):
                continue
            proc_body.append(line)

        proc_sql_text = '\n'.join(proc_body).strip()

        if not proc_sql_text.lower().startswith("replace procedure") and not proc_sql_text.lower().startswith("create procedure"):
            print(f"⚠️ PROC file does not contain REPLACE/CREATE PROCEDURE, skipping: {sql_file}")
            continue

        # Write to temp
        temp_proc_file = "temp_proc_script.sql"
        with open(temp_proc_file, "w") as f:
            f.write(proc_sql_text + "\n")

        run_file = temp_proc_file
    else:
        print(f"\n🚀 Executing SQL file: {sql_file}")

        temp_sql_file = "temp_script.sql"
        with open(temp_sql_file, "w") as f:
            f.write(final_sql + "\n")

        run_file = temp_sql_file

    # Build bteq command
    if executionenv.upper() == "UAT":
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},RpSQC\\$c_4dwv;
.osource {run_file};
.logoff;
.quit;
EOF
"""
    elif executionenv.upper() == "PRD":
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},\\$_bdgE7r1#Tr;
.osource {run_file};
.logoff;
.quit;
EOF
"""
    else:
        bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},{pwd};
.osource {run_file};
.logoff;
.quit;
EOF
"""

    # Run bteq
    result = subprocess.run(bteq_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    print("📜 BTEQ Output:\n", result.stdout)
    if result.returncode != 0:
        print(f"❌ Execution failed for {sql_file}:\n", result.stderr)
        exit(result.returncode)

print("\n✅ All SQL & PROC files executed successfully.")
