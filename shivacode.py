import os
import re
import xml.etree.ElementTree as ET
import subprocess
import glob
import datetime

# Settings
DEBUG_VERBOSE = True   # Set to False if you want less verbose
SHOW_TIMESTAMPS = True

# Helper: print with timestamp
def log(msg):
    if SHOW_TIMESTAMPS:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] {msg}")
    else:
        print(msg)

# Get execution environment
executionenv = os.getenv("ENV_ID", "")
env_id = f"_{executionenv}" if executionenv.upper() in ('DEV2', 'DEV', 'INT', 'QA') else ""

# Teradata credentials
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

if not all([host, user, pwd]):
    log("❌ Missing TERADATA environment variables")
    exit(1)

# Cleanup duplicate update.xml
base_path = "Teradata/src"
for xml_file in glob.glob("**/update*.xml", recursive=True):
    if not xml_file.endswith("Teradata/src/update.xml"):
        log(f"🗑️ Removing outdated update file: {xml_file}")
        os.remove(xml_file)

# Parse update.xml
update_xml_path = os.path.join(base_path, "update.xml")
tree = ET.parse(update_xml_path)
root = tree.getroot()
ns = {"db": "http://www.liquibase.org/xml/ns/dbchangelog"}
sql_files = [elem.attrib["file"] for elem in root.findall("db:include", ns)]

if not sql_files:
    log("⚠️ No SQL files found in update.xml")
    exit(0)

log("📂 SQL files to execute/deploy:")
for file in sql_files:
    log(f"  * {file}")

# Process each file
for sql_file in sql_files:
    full_path = os.path.join(base_path, sql_file)

    if not os.path.exists(full_path):
        log(f"⚠️ Skipping missing SQL file: {full_path}")
        continue

    with open(full_path, "r") as f:
        content = f.read()
        final_sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), content).strip()

    # PROC detection
    is_proc = sql_file.startswith("PROC/HSPROCS/")
    proc_marker_found = bool(re.search(r'\b(REPLACE\s+PROCEDURE|CREATE\s+PROCEDURE)\b', final_sql, re.IGNORECASE))

    temp_file = "temp_script.sql"
    with open(temp_file, "w") as f:
        if is_proc:
            log(f"\n🚀 Deploying PROCEDURE file: {sql_file}")

            if not proc_marker_found:
                log(f"⚠️ WARNING: No REPLACE/CREATE PROCEDURE found — skipping PROC file: {sql_file}")
                continue

            f.write(".SET SESSION SQLFLAG = TERADATA;\n")
            f.write(".SET DELIMITER $$\n\n")

            f.write(final_sql)
            f.write("\n$$\n")

            if DEBUG_VERBOSE:
                log(f"🛠️ PROC content prepared with $$ terminator.")
        else:
            log(f"\n🚀 Executing SQL file: {sql_file}")
            f.write(final_sql + "\n")

    # Build bteq command
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

    # Run bteq
    log("📜 BTEQ Output:")
    result = subprocess.run(bteq_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    print(result.stdout)
    if result.returncode != 0:
        log(f"❌ Execution failed for {sql_file}")
        print(result.stderr)
        exit(result.returncode)

log("\n✅ All SQL & PROC files executed successfully.")
