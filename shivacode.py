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
        else:
            app_log.debug("✅ Snowflake connection was successfully created")
            print("✅ Snowflake Connection Successful!")
        
        return ctx
    except Exception as e:
        app_log.error(f"Error in sf_create_ctx: {str(e)}")
        return None  # Ensure function returns None if connection fails




def sf_run_query(ctx=None, query=None):
    try:
        if ctx is None:
            ctx = sf_create_ctx()
        
        # Ensure ctx is not None before calling cursor()
        if ctx is None:
            app_log.error("❌ Snowflake connection failed. Cannot execute query.")
            return None, "FAILURE"
        
        cur = ctx.cursor()
        
        if query is None:
            query_path = get_conf_val("sql_config", "SQL_PATH")
            with open(query_path, 'r') as file:
                query = file.read().replace('\n', ' ')
        
        cur.execute(query)
        output_df = cur.fetch_pandas_all()

        if not output_df.empty:
            status = "SUCCESS"
            app_log.info("✅ bsd_monitor.sf_run_query successfully ran")
            app_log.debug(f"bsd_monitor.sf_run_query has returned df: {output_df}")
        else:
            status = "FAILURE"
            app_log.error("❌ bsd_monitor.sf_run_query failed to return data")
        
        return output_df, status
    except Exception as e:
        app_log.error(f"❌ bsd_monitor.sf_run_query encountered an error: {str(e)}")
        return None, "FAILURE"
