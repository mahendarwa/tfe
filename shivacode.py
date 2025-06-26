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

# ✅ Delete old update.xml if exists
if os.path.exists(update_xml_path):
    try:
        os.remove(update_xml_path)
        print(f"🗑️ Deleted old update.xml: {update_xml_path}")
    except Exception as e:
        print(f"❌ Failed to delete update.xml: {e}")
        exit(1)
else:
    print(f"ℹ️ No update.xml file found at: {update_xml_path} (nothing to delete)")

# Re-check if update.xml still needed to be parsed
if not os.path.exists(update_xml_path):
    print("⚠️ Skipping XML parse — update.xml no longer exists.")
    exit(0)

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
