import os
import re
import getpass
import snowflake.connector

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

def sf_create_ctx(oauth_token=None):
    try:
        env = "dev"
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
        print("Snowflake connection established successfully.")
        return ctx
    except Exception as e:
        print(f"Snowflake connection failed: {str(e)}")
        return None

def get_conf_val(section, key):
    config = {
        "sf_config": {
            "HIPAM_AUTH_ACC": "apadmin",
            "SF_USER": "SRVC_BSD_APP_DEV",
            "SF_ACCOUNT_ID": "dtccriskdev",
            "SF_URL": "dtccriskdev.us-east-1.privatelink.snowflakecomputing.com",
            "SF_WAREHOUSE": "BSD_ADHOC_WH",
            "SF_DATABASE": "BSD",
            "SF_SCHEMA": "RAW"
        }
    }
    return config.get(section, {}).get(key, "")

if __name__ == "__main__":
    ctx = sf_create_ctx()
    if ctx:
        print("Successfully connected to Snowflake!")
    else:
        print("Failed to connect to Snowflake.")
