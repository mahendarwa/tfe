import argparse, sys
import json
from datetime import datetime
import pytz
import pandas as pd

import deployment.dbt_logger as dbt_logger
import deployment.snowflake_handler as sf_handler

from deployment.deployment_constants import QUERY_DAILY_PLAN_DETAILS
from deployment.deployment_constants import LQT_DB, LQT_SCHEMA
from deployment.deployment_constants import ARIP_DB, ARIP_SCHEMA
from deployment.deployment_constants import SRC_DB_LIST, CALC_DB_LIST
from deployment.deployment_constants import LQT_JOB_LOG_TABLE, ARI_JOB_LOG_TABLE

log = dbt_logger.initialize(__name__)

sf_connection = None
sf_cursor = None

business_date = None
slice_id = None
command = None  # New variable to hold command
host_name = None  # New variable to hold host name
tz = pytz.timezone("US/Eastern")

def parse_args(argv=None):
    """
    Function to parse arguments passed from command line,
    used to set global variables
    :param config: argv
    :return:
    """
    try:
        global business_date, slice_id, command, host_name
        parser = argparse.ArgumentParser()
        parser.add_argument('--slice', nargs='?', default='0', const='0', help='slice')
        parser.add_argument('--bus_dt', nargs='?', default=datetime.now().date(), const=datetime.now().date(),
                            help="Business Date", type=str)
        parser.add_argument('--command', nargs='?', default='', const='', help="Command to issue, e.g., 'shutdown'")
        parser.add_argument('--host_name', nargs='?', default='', const='', help="Target host name")
        
        args = parser.parse_args(argv)
        business_date = args.bus_dt
        slice_id = int(args.slice)
        command = args.command
        host_name = args.host_name
        return
    except Exception as e:
        log.exception("deployment.start_of_day_run.parse_args - Exception: %s", str(e))
        raise e

def issue_host_command():
    """
    Issues a command to a specified host by updating the HOST_COMMAND column in the database table.
    """
    try:
        global sf_cursor
        if sf_cursor is None:
            sf_cursor = sf_handler.get_sf_cursor()
        
        if not command or not host_name:
            log.error("Command or host name not provided.")
            return
        
        query = f"""
            UPDATE ARIP.OPS.DBT_HOSTS
            SET HOST_COMMAND = '{command}'
            WHERE HOST_NAME = '{host_name}'
        """
        log.info("Executing host command update: %s", query)
        sf_cursor.execute(query)
        sf_connection.commit()
        log.info("Successfully issued command '%s' to host '%s'", command, host_name)
    except Exception as e:
        log.exception("deployment.start_of_day_run.issue_host_command - Exception: %s", str(e))
        raise e

def get_daily_plan():
    """
    Function executes sql query to retrieve daily_plan from union of ARIP & LQT Snowflake Tables
    :param config:
    :return: results: Pandas.DataFrame
    """
    try:
        global sf_cursor
        if sf_cursor is None:
            sf_cursor = sf_handler.get_sf_cursor()
        log.info("deployment.start_of_day_run.get_daily_plan - executing query - %s", QUERY_DAILY_PLAN_DETAILS)
        sf_cursor.execute(QUERY_DAILY_PLAN_DETAILS)
        log.info("deployment.start_of_day_run.get_daily_plan - fetched results for query - %s",
                 QUERY_DAILY_PLAN_DETAILS)
        results = sf_cursor.fetch_pandas_all()
        results.columns = map(str.lower, results.columns)
        return results
    except Exception as e:
        log.exception("deployment.start_of_day_run.get_daily_plan - Failed to get daily plan - Exception: %s", str(e))
        if 'OAuth access token expired' in str(e):
            log.error("deployment.start_of_day_run.get_daily_plan - Access token expired, refreshing.")
            get_daily_plan()

def write_job_log_to_sf(df=None, db=None, schema=None, table=None):
    """
    Writes the job log details from a Pandas DataFrame to a Snowflake table.
    :param config: df: Pandas DataFrame, db: string, schema: string, table: string
    :return:
    """
    try:
        global sf_connection, sf_cursor
        if sf_connection is None:
            sf_connection = sf_handler.get_sf_connection(db=LQT_DB, schema=LQT_SCHEMA)
        if sf_cursor is None:
            sf_cursor = sf_handler.get_sf_cursor()
        
        log.info("Preparing to insert into table %s.%s.%s", db, schema, table)
        query = f"INSERT INTO {db}.{schema}.{table} (JOB_NAME, BUS_DT, SLICE_ID, STATUS, EXPECTED_DEP, " \
                f"ACTUAL_DEP, DB_NAME, ACTIVE, RUN_CNT, EXPECTED_START_TIME, HOST_COMMAND) " \
                f"SELECT $1 as JOB_NAME, $2 as BUS_DT, $3 as SLICE_ID, $4 as STATUS, PARSE_JSON($5) as EXPECTED_DEP, " \
                f"PARSE_JSON($6) as ACTUAL_DEP, $7 as DB_NAME, $8 as ACTIVE, $9 as RUN_CNT, $10 as EXPECTED_START_TIME, " \
                f"'{command}' as HOST_COMMAND FROM VALUES"
        # Data preparation
        data_list = [
            f" ('{row.job_name}', '{row.bus_dt}', '{row.slice_id}', '{row.status}', " \
            f"'{row.expected_dep}', '{row.actual_dep}', '{row.db_name}', '{row.active}', '-1', " \
            f"'{row.expected_start_time}' )"
            for _, row in df.iterrows()
        ]
        query += " ,".join(data_list)
        sf_cursor.execute(query)

        # Update run count
        query2 = f"""
            UPDATE {db}.{schema}.{table} t
            SET RUN_CNT=n.NEW_RUN_CNT
            FROM (
                SELECT BUS_DT, SLICE_ID, RUN_CNT, RUN_ID, JOB_NAME, ROW_NUMBER() OVER(
                    PARTITION BY BUS_DT, JOB_NAME, SLICE_ID ORDER BY RUN_ID) as NEW_RUN_CNT
                FROM {db}.{schema}.{table}
            ) AS n
            WHERE t.BUS_DT=n.BUS_DT AND t.JOB_NAME=n.JOB_NAME AND t.SLICE_ID=n.SLICE_ID AND t.RUN_ID=n.RUN_ID
        """
        sf_cursor.execute(query2)
        sf_connection.commit()
    except Exception as e:
        log.exception("Error in write_job_log_to_sf: %s", str(e))
        raise e

def main():
    """
    Main Function to execute daily plan processing or issue host command
    """
    try:
        log.info("Starting main function")
        parse_args(argv=sys.argv[1:])
        
        # Issue command if provided
        if command:
            issue_host_command()
        
        # Process daily plan
        df_dict = generate_log_details()
        for key, df in df_dict.items():
            if key in CALC_DB_LIST:
                db = LQT_DB
                schema = LQT_SCHEMA
                table = LQT_JOB_LOG_TABLE
            elif key in SRC_DB_LIST:
                db = ARIP_DB
                schema = ARIP_SCHEMA
                table = ARI_JOB_LOG_TABLE
            else:
                continue  # Skip undefined entries
            write_job_log_to_sf(df=df, db=db, schema=schema, table=table)
    except Exception as e:
        log.exception("Error in main function: %s", str(e))
        raise e

if __name__ == "__main__":
    log.info("Initializing Start of day run to populate log tables from Daily plan")
    main()
else:
    parse_args(argv=sys.argv[1:])
