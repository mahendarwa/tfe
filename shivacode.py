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
            app_log.error("❌ Snowflake connection failed: ctx is None.")
            print("❌ Snowflake Connection Failed!")
            return None

        # Explicitly set warehouse and validate it exists
        cur = ctx.cursor()

        try:
            cur.execute(f"USE WAREHOUSE {warehouse_name};")
            cur.execute("SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();")
            result = cur.fetchall()
            if result:
                print(f"✅ Active Warehouse: {result[0][0]}, Database: {result[0][1]}, Schema: {result[0][2]}")
                app_log.debug(f"✅ Snowflake connection successful with Warehouse: {result[0][0]}")
            else:
                print("❌ Warehouse not active. Verify warehouse permissions.")
                return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            app_log.error(f"❌ Error setting warehouse: {str(e)}")
            return None
        finally:
            cur.close()

        return ctx
    except Exception as e:
        app_log.error(f"Error in sf_create_ctx: {str(e)}")
        return None







def sf_run_query(ctx=None, query=None):
    """
    Runs the Snowflake query and puts it into a dataframe.
    """
    try:
        if ctx is None:
            ctx = sf_create_ctx()
            if ctx is None:
                app_log.error("❌ Snowflake connection failed, cannot execute query.")
                return None, "FAILURE"

        cur = ctx.cursor()

        if query is None:
            query_path = get_conf_val("sql_config", "SQL_PATH")
            with open(query_path, 'r') as file:
                query = file.read().replace('\n', ' ')

        cur.execute(query)
        output_df = cur.fetch_pandas_all()

        if output_df is None or output_df.empty:
            status = 'FAILURE'
            app_log.error("❌ Query execution failed, no data returned.")
        else:
            status = 'SUCCESS'
            app_log.info("✅ Query executed successfully.")
        
        return output_df, status
    except Exception as e:
        app_log.error(f"❌ Error executing query: {str(e)}")
        return None, "FAILURE"
