import os
import xml.etree.ElementTree as ET
import teradatasql

host = os.environ.get("TERADATA_HOST")
user = os.environ.get("TERADATA_USER")
pwd = os.environ.get("TERADATA_PASSWORD")
env_id = os.environ.get("ENV_ID", "DEV")

if not host or not user or not pwd:
    print("❌ Missing TERADATA_HOST, USER, or PASSWORD.")
    exit(1)

xml_path = "Teradata/src/update.xml"
if not os.path.exists(xml_path):
    print(f"❌ update.xml not found at path: {xml_path}")
    exit(1)

tree = ET.parse(xml_path)
root = tree.getroot()
ns = {'db': 'http://www.liquibase.org/xml/ns/dbchangelog'}
sql_files = [elem.attrib['file'] for elem in root.findall('db:include', ns)]

if not sql_files:
    print("⚠️ No SQL files found in update.xml")
    exit(0)

print("✅ SQLs to execute:")
for f in sql_files:
    print(f" - {f}")

try:
    with teradatasql.connect(host=host, user=user, password=pwd) as conn:
        print("✅ Connected to Teradata")
        for sql_file in sql_files:
            full_path = os.path.join("Teradata/src", sql_file)
            if not os.path.exists(full_path):
                print(f"❌ SQL file not found: {full_path}")
                exit(1)

            print(f"📂 Executing: {full_path}")
            with open(full_path, "r") as f:
                sql = f.read()

            # Replace tokens
            sql = sql.replace("${env.id.upper}", env_id.upper())
            sql = sql.replace("${env.id.lower}", env_id.lower())
            sql = sql.replace("${env.id}", env_id)

            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    print("✅ Success")
            except Exception as e:
                print(f"❌ SQL Error in {sql_file}:\n{e}")
                exit(1)
except Exception as e:
    print(f"❌ Connection failed:\n{e}")
    exit(1)
