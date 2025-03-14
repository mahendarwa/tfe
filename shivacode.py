import os
import re
import getpass
import snowflake.connector
import datetime

def get_env():
    env = None
    os_env = os.environ.get("DTCC_SERVER_ENVIRONMENT", "")

    if os_env == "DEVELOPMENT":
        env = "dev"
    elif os_env == "QA":
        env = "qa"
    elif os_env == "PRODUCTION":
        env = "prod"

    print(f"Detected environment: {env}")
    return env

def sanitize_input(input_str):
    return re.sub(r'[^a-zA-Z0-9_-]', '', input_str)

def chk_srvc_user():
    curr_user = getpass.getuser()
    hipam_auth_user = get_conf_val("sf_config", "HIPAM_AUTH_ACC")
    return curr_user == hipam_auth_user

def sf_get_oauth_token(client_id, sf_acc_nm):
    try:
        if not chk_srvc_user():
            raise Exception("Unauthorized user")

        client_id = sanitize_input(client_id).lower()
        sf_acc_nm = sanitize_input(sf_acc_nm).lower()
        args = f"/sps/admin/bin/spsoauth.sh -c {client_id} -d CORP -u {sf_acc_nm} -s session:role-any"
        oauth_token = os.popen(args).read().strip()
        return oauth_token
    except Exception as e:
        print(f"Error obtaining OAuth token: {str(e)}")
        return None

def set_proxies():
    try:
        env = get_env()
        url_env = env if env in ["dev", "qa"] else ""

        if "HTTPS_PROXY" not in os.environ:
            os.environ["HTTPS_PROXY"] = f"http://proxy.us-east-1.app{url_env}.dtcc.org:8080"
        if "HTTP_PROXY" not in os.environ:
            os.environ["HTTP_PROXY"] = f"http://proxy.us-east-1.app{url_env}.dtcc.org:8080"
        if "NO_PROXY" not in os.environ:
            os.environ["NO_PROXY"] = "privatelink.snowflakecomputing.com"

        print("Proxy settings applied successfully.")
    except Exception as e:
        print(f"Error setting proxy: {str(e)}")

def get_conf_val(section, key):
    config = {
        "sf_config": {
            "HIPAM_AUTH_ACC": "apadmin",
            "SF_USER": "SRVC_ARIP_APP_DEV",
            "SF_ACCOUNT_ID": "dtccriskdev",
            "SF_URL": "dtccriskdev.us-east-1.snowflakecomputing.com",
            "SF_WAREHOUSE": "ARIP_APP_WH",
            "SF_DATABASE": "ARIP",
            "SF_SCHEMA": "AFRS"
        }
    }
    return config.get(section, {}).get(key, "")

def validate_config():
    """ Validate and print configuration values """
    config_keys = ["HIPAM_AUTH_ACC", "SF_USER", "SF_ACCOUNT_ID", "SF_URL", "SF_WAREHOUSE", "SF_DATABASE", "SF_SCHEMA"]
    
    print("\n🔍 **Validating Configuration**")
    for key in config_keys:
        value = get_conf_val("sf_config", key)
        if not value:
            print(f"❌ Missing configuration: {key}")
        else:
            print(f"✅ {key}: {value}")

def sf_create_ctx(oauth_token=None):
    try:
        set_proxies()
        validate_config()
        
        env = get_env()
        client_id = f"snowflake_{env}"
        sf_acc_nm = get_conf_val("sf_config", "SF_USER")

        if oauth_token is None:
            oauth_token = sf_get_oauth_token(client_id, sf_acc_nm)

        ctx = snowflake.connector.connect(
            user=get_conf_val("sf_config", "SF_USER").lower(),
            host=get_conf_val("sf_config", "SF_URL"),
            account=get_conf_val("sf_config", "SF_ACCOUNT_ID"),
            authenticator="oauth",
            token=oauth_token,
            warehouse=get_conf_val("sf_config", "SF_WAREHOUSE"),
            database=get_conf_val("sf_config", "SF_DATABASE"),
            schema=get_conf_val("sf_config", "SF_SCHEMA")
        )
        print("\n✅ Snowflake connection established successfully.")
        return ctx
    except Exception as e:
        print(f"❌ Snowflake connection failed: {str(e)}")
        return None

def get_business_date():
    """ Get today's business date assuming it's a working day """
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')

def check_snowflake_data(ctx):
    """ Check if SLC_TM (sliceid) and DT_KEY exist for the business date """
    try:
        cursor = ctx.cursor()
        
        bus_dt = get_business_date()
        print(f"\n🔍 Checking data for Business Date: {bus_dt}")

        query = f"""
        SELECT SLC_TM, DT_KEY
        FROM ARIP.AFRS.CREDIT_RATING
        WHERE BUS_DT = '{bus_dt}';
        """

        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print("\n✅ Data Found for the Business Date!")
            for row in results:
                sliceid, dt_key = row
                print(f"📌 SLC_TM (sliceid): {sliceid}, DT_KEY: {dt_key}")
        else:
            print("\n❌ No Data Found for the Business Date!")

        cursor.close()

    except Exception as e:
        print(f"❌ Error querying Snowflake: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 **Starting Snowflake Connection and Data Validation**")
    ctx = sf_create_ctx()
    
    if ctx:
        print("\n🎯 **Successfully connected to Snowflake!**")
        check_snowflake_data(ctx)
        ctx.close()
    else:
        print("\n❌ **Failed to connect to Snowflake.**")
