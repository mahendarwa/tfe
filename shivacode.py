import snowflake.connector

# Snowflake connection details from the screenshot
SF_USER = "SRVC_BSD_APP_DEV"
SF_ACCOUNT = "dtccriskdev"
SF_URL = "dtccriskdev.us-east-1.privatelink.snowflakecomputing.com"
SF_WAREHOUSE = "BSD_ADHOC_WH"
SF_DATABASE = "BSD"
SF_SCHEMA = "RAW"

try:
    # Establish connection
    conn = snowflake.connector.connect(
        user=SF_USER,
        account=SF_ACCOUNT,
        host=SF_URL,
        warehouse=SF_WAREHOUSE,
        database=SF_DATABASE,
        schema=SF_SCHEMA,
        authenticator="oauth",  # Modify based on authentication method
    )
    
    # Check if the connection is successful
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_VERSION()")  # Test query
    version = cur.fetchone()
    
    print(f"Connected to Snowflake. Version: {version[0]}")

    # Close the connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"Failed to connect to Snowflake: {e}")
