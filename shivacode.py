import os
import re
import teradatasql

# Hardcoded environment
executionenv = "DEV"  # Change to UAT / PROD / INT etc. to test other cases
sql_file = "Teradata/src/DDL/SDO_EDI_834_MBR_PCP_HIST_20250709.sql"

# Derive env_id replacement string
if executionenv.upper() in ('DEV2', 'DEV', 'INT', 'QA'):
    env_id = "_" + executionenv
elif executionenv.upper() in ('UAT', 'PRD', 'PROD'):
    env_id = ""
else:
    print("❌ Unsupported execution environment.")
    exit(1)

# Teradata credentials
host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

if not host or not user or not pwd:
    print("❌ Missing TERADATA_HOST, USER, or PASSWORD.")
    exit(1)

# Check SQL file
if not os.path.exists(sql_file):
    print(f"❌ SQL file not found: {sql_file}")
    exit(1)

# Read SQL
with open(sql_file, "r") as f:
    sql = f.read()

# Replace ${env.id.upper} with proper value
sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), sql)

# Debug output
print("📄 Final SQL:")
print(sql)

# Connect and execute each statement
try:
    with teradatasql.connect(host=host, user=user, password=pwd) as conn:
        for statement in sql.split(";"):
            statement = statement.strip()
            if not statement:
                continue
            try:
                with conn.cursor() as cur:
                    cur.execute(statement)
                    print(f"✅ Executed:\n{statement}\n")
            except Exception as e:
                print(f"❌ SQL Error:\n{statement}\n{e}")
                exit(1)
except Exception as e:
    print(f"❌ Connection failed:\n{e}")
    exit(1)
