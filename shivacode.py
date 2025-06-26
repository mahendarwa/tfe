import os
import re
import xml.etree.ElementTree as ET

# Get execution environment
executionenv = os.getenv("ENV_ID", "")
env_id = f"_{executionenv}" if executionenv.upper() in ("DEV2", "DEV", "INT", "QA", "UAT") else ""

# Teradata credentials (still validated, can remove if not needed)
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd  = os.getenv("TERADATA_PASSWORD")

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
    print("⚠️ No SQL files found in update.xml")
    exit(0)

# Print resolved full paths
print("📄 SQL file full paths:")
for sql_file in sql_files:
    full_path = os.path.join(base_path, sql_file)
    if os.path.exists(full_path):
        print(f"✅ {full_path}")
    else:
        print(f"❌ Missing: {full_path}")
