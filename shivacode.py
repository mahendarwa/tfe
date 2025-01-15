def sf_create_ctx(oauth_token=None):
    try:
        env = get_env()
        client_id = "snowflake_" + env
        sf_acc_nm = get_conf_val("sf_config", "SF_USER")

        print(f"Configured warehouse: {get_conf_val('sf_config', 'SF_WAREHOUSE')}")

        if oauth_token is None:
            oauth_token = sf_get_oauth_token(client_id, sf_acc_nm)

        set_proxies()
        warehouse_name = get_conf_val("sf_config", "SF_WAREHOUSE")

        ctx = sfc.connect(
            user=get_conf_val("sf_config", "SF_USER").lower(),
            host=get_conf_val("sf_config", "SF_URL"),
            account=get_conf_val("sf_config", "SF_ACCOUNT_ID"),
            authenticator="oauth",
            token=oauth_token,
            warehouse=warehouse_name,
            database=get_conf_val("sf_config", "SF_DATABASE"),
            schema=get_conf_val("sf_config", "SF_SCHEMA")
        )

        if ctx is None:
            app_log.error("Snowflake connection failed. ctx is None.")
            print("❌ Snowflake Connection Failed!")
            return None

        # Explicitly set warehouse
        cur = ctx.cursor()
        cur.execute(f"USE WAREHOUSE {warehouse_name};")
        cur.close()

        app_log.debug("✅ Snowflake connection and warehouse set successfully")
        print("✅ Snowflake Connection and Warehouse Set Successfully!")

        return ctx
    except Exception as e:
        app_log.error(f"Error in sf_create_ctx: {str(e)}")
        return None
