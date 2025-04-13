- name: 🚀 Deploy SQL files to Teradata
  run: |
    echo "📁 Scanning for .sql files in teradata_deploy/src..."
    python3 <<EOF
    import os
    import teradatasql

    host = os.getenv("TERADATA_HOST")
    user = os.getenv("TERADATA_USER")
    pwd  = os.getenv("TERADATA_PASSWORD")

    deploy_path = "teradata_deploy/src"
    print(f"🔍 Connecting to Teradata at {host} as {user}")
    
    try:
        with teradatasql.connect(host=host, user=user, password=pwd) as conn:
            cursor = conn.cursor()
            for root, _, files in os.walk(deploy_path):
                for file in files:
                    if file.endswith(".sql"):
                        full_path = os.path.join(root, file)
                        print(f"📄 Executing {full_path}")
                        with open(full_path, 'r') as sql_file:
                            sql = sql_file.read()
                            cursor.execute(sql)
                            print("✅ Executed successfully")
            cursor.close()
    except Exception as e:
        print("❌ Deployment failed:", e)
        exit(1)
    EOF
