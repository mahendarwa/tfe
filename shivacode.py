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

# Print resolved full paths (skip PROC/HSPROCS)
for sql_file in sql_files:
    if sql_file.startswith("PROC/HSPROCS/"):
        continue  # skip these

    if sql_file in printed:
        continue  # skip duplicates

    printed.add(sql_file)
    full_path = os.path.join(base_path, sql_file)
    if os.path.exists(full_path):
        print(f"✅ {full_path}")
    else:
        print(f"❌ Missing: {full_path}")

# ✅ Delete update.xml after everything is printed
try:
    os.remove(update_xml_path)
    print(f"\n🗑️ Deleted update.xml after processing: {update_xml_path}")
except Exception as e:
    print(f"❌ Failed to delete update.xml: {e}")
    exit(1)
