- name: 🔌 Test Teradata connection via Python
  run: |
    echo "🧪 Verifying Teradata connectivity using teradatasql..."
    python3 <<EOF
import os
import teradatasql

host = os.getenv("TERADATA_HOST")
user = os.getenv("TERADATA_USER")
pwd = os.getenv("TERADATA_PASSWORD")

print("🔍 Connecting to", host, "with user:", user)

try:
    with teradatasql.connect(host=host, user=user, password=pwd) as conn:
        print("✅ Connected! Running SELECT CURRENT_DATE...")
        with conn.cursor() as cur:
            cur.execute("SELECT CURRENT_DATE")
            print("🗓️ Result:", cur.fetchone()[0])
except Exception as e:
    print("❌ Connection failed:", e)
    exit(1)
EOF
