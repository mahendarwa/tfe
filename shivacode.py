import snowflake.connector

def sf_create_ctx(oauth_token=None):
    """
    Creates the Snowflake connector based on the values defined in the config files
    """
    try:
        env = get_env()
        client_id = "snowflake_" + env
        sf_acc_nm = get_conf_val("sf_config", "SF_USER")

        print(f"Configured warehouse: {get_conf_val('sf_config', 'SF_WAREHOUSE')}")
        
        if oauth_token is None:
            oauth_token = sf_get_oauth_token(client_id, sf_acc_nm)

        set_proxies()
        warehouse_name = get_conf_val("sf_config", "SF_WAREHOUSE")

        # Establish Snowflake Connection
        ctx = snowflake.connector.connect(
            user=get_conf_val("sf_config", "SF_USER").lower(),
            host=get_conf_val("sf_config", "SF_URL"),
            account=get_conf_val("sf_config", "SF_ACCOUNT_ID"),
            authenticator="oauth",
            token=oauth_token,
            warehouse=warehouse_name,
            database=get_conf_val("sf_config", "SF_DATABASE"),
            schema=get_conf_val("sf_config", "SF_SCHEMA"),
        )

        # Check if connection is successful by running a test query
        cur = ctx.cursor()
        cur.execute("SELECT CURRENT_VERSION()")  # Snowflake test query
        version = cur.fetchone()
        
        print(f"✅ Snowflake Connection Successful! Version: {version[0]}")
        app_log.debug("bsd_monitor.sf_create_ctx - Snowflake connection successful")

        cur.close()
        return ctx

    except Exception as e:
        print(f"❌ Snowflake Connection Failed: {str(e)}")
        app_log.error(f"bsd_monitor.sf_create_ctx has encountered an error: {str(e)}")
        return None  # Return None if connection fails
