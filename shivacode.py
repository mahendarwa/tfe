- name: Set ENV_ID
  run: echo "ENV_ID=DEV" >> $GITHUB_ENV

- name: 🌿 Execute SQLs from update.xml dynamically
  run: |
    pip install teradatasql
    python3 - <<EOF
import os
import xml.etree.ElementTree as ET
import teradatasql

host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")
env_id = os.getenv("ENV_ID", "DEV")

if not host or not user or not pwd:
    print("❌ Missing TERADATA_HOST, USER, or PASSWORD.")
    exit(1)

tree = ET.parse("Teradata/src/update.xml")
root = tree.getroot()
ns = {'db': 'http://www.liquibase.org/xml/ns/dbchangelog'}
sql_files = [elem.attrib['file'] for elem in root.findall('db:include', ns)]

if not sql_files:
    print("⚠️ No SQL files found in update.xml")
    exit(0)

with teradatasql.connect(host=host, user=user, password=pwd) as conn:
    print("✅ Connected to Teradata")

    for sql_file in sql_files:
        full_path = os.path.join("Teradata/src", sql_file)
        print(f"📁 Executing: {full_path}")

        with open(full_path, "r") as f:
            sql = f.read()

        # 🔁 Replace placeholders before execution
        sql = sql.replace("${env.id.upper}", env_id.upper())
        sql = sql.replace("${env.id.lower}", env_id.lower())

        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                print("✅ Done.")
        except Exception as e:
            print(f"❌ Error executing {sql_file}: {e}")
            exit(1)
EOF
