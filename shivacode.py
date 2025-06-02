- name: 🧪 Execute SQLs from update.xml dynamically
  env:
    TERADATA_HOST: ${{ secrets.TERADATA_HOST }}
    TERADATA_USER: ${{ secrets.TERADATA_USER }}
    TERADATA_PASSWORD: ${{ secrets.TERADATA_PASSWORD }}
  run: |
    echo "📄 Parsing update.xml and running included SQL files..."
    pip install teradatasql
    python3 - <<EOF
import os
import re
import xml.etree.ElementTree as ET
import teradatasql

host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

# Parse update.xml to extract SQL files
tree = ET.parse("Teradata/src/update.xml")
root = tree.getroot()
ns = {'db': 'http://www.liquibase.org/xml/ns/dbchangelog'}
sql_files = [elem.attrib['file'] for elem in root.findall('db:include', ns)]

if not sql_files:
    print("⚠️ No SQL files found in update.xml")
    exit(0)

# Connect to Teradata and execute each SQL file
with teradatasql.connect(host=host, user=user, password=pwd) as conn:
    print("✅ Connected to Teradata")

    for sql_path in sql_files:
        full_path = os.path.join("Teradata/src", sql_path)
        print(f"📂 Executing SQL file: {full_path}")

        with open(full_path, "r") as f:
            sql_content = f.read()

        try:
            with conn.cursor() as cur:
                cur.execute(sql_content)
                print(f"✅ Successfully executed: {sql_path}")
        except Exception as e:
            print(f"❌ Failed to execute {sql_path}: {e}")
            exit(1)
EOF
