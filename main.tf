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
tz = pytz.timezone("US/Eastern")

def parse_args(argv=None):
    """
    Function to parse arguments passed from command line,
    used to set global variables
    :param config: argv
    :return:
    """
    try:
        global business_date
        global slice_id
        parser = argparse.ArgumentParser()
        parser.add_argument('--slice',
                            nargs='?',
                            default='0', const='0',
                            help='slice')
        parser.add_argument('--bus_dt',
                            nargs='?',
                            default=datetime.now().date(),
                            const=datetime.now().date(),
                            help="Business Date",
                            type=str)
        args = parser.parse_args(argv)
        business_date = args.bus_dt
        slice_id = int(args.slice)
        return
    except Exception as e:
        log.exception("deployment.start_of_day_run.parse_args - Exception: %s", str(e))
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
            log.error("deployment.start_of_day_run.get_daily_plan - Access token has expired. Refreshing the token..")
            get_daily_plan()

def write_job_log_to_sf(df=None, db=None, schema=None, table=None):
    """
    Function given Pandas DataFrame and Snowflake Table Details; uses Snowflake Cursor
    to write to Snowflake Table
    :param config: df: Pandas DataFrame, db: string, schema: string, table: string
    :return:
    """
    try:
        global sf_connection
        global sf_cursor
        if sf_connection is None:
            sf_connection = sf_handler.get_sf_connection(db=LQT_DB, schema=LQT_SCHEMA)
        if sf_cursor is None:
            sf_cursor = sf_handler.get_sf_cursor()
        log.info("deployment.start_of_day_run.write_job_log_to_sf - preparing query to insert in table - %s.%s.%s",
                 db, schema, table)
        query = f"INSERT INTO {db}.{schema}.{table} (JOB_NAME, BUS_DT, SLICE_ID, STATUS, EXPECTED_DEP, " \
                f"ACTUAL_DEP, DB_NAME, ACTIVE, RUN_CNT, EXPECTED_START_TIME) SELECT $1 as JOB_NAME, $2 as BUS_DT," \
                f"$3 as SLICE_ID, $4 as STATUS, PARSE_JSON($5) as EXPECTED_DEP, PARSE_JSON($6) as ACTUAL_DEP," \
                f"$7 as DB_NAME, $8 as ACTIVE, $9 as RUN_CNT, $10 as EXPECTED_START_TIME FROM VALUES"
        data_list = []
        for index, val in df.iterrows():
            q = f" ('{df['job_name'].iloc[index]}', '{df['bus_dt'].iloc[index]}', '{df['slice_id'].iloc[index]}'," \
                f"'{df['status'].iloc[index]}', '{df['expected_dep'].iloc[index]}', '{df['actual_dep'].iloc[index]}'," \
                f"'{df['db_name'].iloc[index]}', '{df['active'].iloc[index]}', '-1'," \
                f"'{df['expected_start_time'].iloc[index]}' )"
            data_list.append(q)
        query = query + " ,".join(data_list)
        log.debug("deployment.start_of_day_run.write_job_log_to_sf - Execute insert query - \n %s ", query)
        sf_cursor.execute(query)

        query2 = f"UPDATE {db}.{schema}.{table} t SET RUN_CNT=n.NEW_RUN_CNT FROM( SELECT BUS_DT," \
                 f" SLICE_ID, RUN_CNT, RUN_ID, JOB_NAME, ROW_NUMBER() OVER( PARTITION BY BUS_DT, JOB_NAME, SLICE_ID " \
                 f" ORDER BY RUN_ID ) as NEW_RUN_CNT FROM {db}.{schema}.{table}) AS n WHERE t.BUS_DT=" \
                 f"n.BUS_DT and t.JOB_NAME=n.JOB_NAME and t.SLICE_ID=n.SLICE_ID and t.RUN_ID=n.RUN_ID"
        sf_cursor.execute(query2)
        sf_connection.commit()
        log.info("deployment.start_of_day_run.write_job_log_to_sf - inserted %d records - in table %s.%s.%s ",
                 df.shape[0], db, schema, table)
    except Exception as e:
        log.exception("deployment.start_of_day_run.write_job_log_to_sf - Exception: %s", str(e))
        raise e

def set_expected_dep(expected_dep=None, daily_plan_df=None, index=None):
    """
    Function given expected_dependencies, DailyPlan DataFrame and index; iterates through
    expected_dependencies to set job name, slice and active flag.
    :param config: expected_dep: ?, daily_plan_df: Pandas DataFrame, index: ?
    :return: expected_dep: ?
    """
    try:
        for i in expected_dep:
            if i["type"] == "job":
                i["bus_dt"] = business_date.strftime('%Y-%m-%d')
                condition = (daily_plan_df['job_name'] == i['job_name']) & \
                            (daily_plan_df['slice'] == i['slice'])  # should fetch one record only
                expct_dep = daily_plan_df[condition]
                if expct_dep.shape[0] > 0:  # TODO recheck logic for active flag
                    i['active'] = expct_dep.loc[index, 'active']
                else:
                    i['active'] = daily_plan_df.loc[index, 'active']
            elif i["type"] == "source":
                i['active'] = daily_plan_df.loc[index, 'active']
        return expected_dep
    except Exception as e:
        log.exception("deployment.start_of_day_run.set_expected_dep - Exception: %s", str(e))
        raise e

def get_log_details(daily_plan_df, db, node_mapper_list):
    """
    Function is provided daily_plan df, db, and node_mapper list; iterates through daily_plan df
    to extract dependency, job and status details; returns node_mapper list
    :param config: daily_plan_df: Pandas DataFrame, db: string, node_mapper_list: list
    :return: node_mapper_list: list
    """
    try:
        for index, row in daily_plan_df.iterrows():
            db_node_mapper = {}
            # look for calculation models
            expected_dep = json.loads(daily_plan_df.loc[index, 'expected_dependency'])
            expected_dep = set_expected_dep(expected_dep=expected_dep, daily_plan_df=daily_plan_df,
                                            index=index)
            db_node_mapper['expected_dep'] = json.dumps(expected_dep)
            db_node_mapper['actual_dep'] = []
            db_node_mapper['job_name'] = daily_plan_df.loc[index, 'job_name']
            db_node_mapper['status'] = 'NEW'
            db_node_mapper['bus_dt'] = business_date
            db_node_mapper['active'] = daily_plan_df.loc[index, 'active']  # TODO discuss if we need active status at log level
            db_node_mapper['slice_id'] = daily_plan_df.loc[index, 'slice']
            db_node_mapper['db_name'] = db
            expected_start_tm = daily_plan_df.loc[index, 'expected_start_time']
            expected_start_dt_str = business_date.strftime('%Y-%m-%d') + ' ' + str(expected_start_tm.hour).zfill(2) + ':' + \
                                    str(expected_start_tm.minute).zfill(2) + ':' + str(expected_start_tm.second).zfill(2)
            expected_start_dt = datetime.strptime(expected_start_dt_str, '%Y-%m-%d %H:%M:%S')
            db_node_mapper['expected_start_time'] = expected_start_dt
            node_mapper_list.append(db_node_mapper)
        return node_mapper_list
    except Exception as e:
        log.exception("deployment.start_of_day_run.get_log_details - Exception: %s", str(e))
        raise e

def generate_log_details():
    """
    Function is provided daily_plan df, db, and node_mapper list; iterates through daily_plan df
    to extract dependency, job and status details; returns node_mapper list
    :param config: daily_plan_df: Pandas DataFrame, db: string, node_mapper_list: list
    :return: node_mapper_list: list
    """
    try:
        manifest_df_dict = {}
        node_mapper = {}
        log.info("deployment.start_of_day_run.generate_log_details - get daily plan manifest")
        # get all the slices
        daily_plan_df = get_daily_plan()
        # get unique db_records
        unique_db_log_name = daily_plan_df['db_name'].unique().tolist()
        log.info("deployment.start_of_day_run.generate_log_details - distinct db names in daily plan table %s",
                 str(unique_db_log_name))
        for db in unique_db_log_name:
            node_mapper_list = []
            db_daily_plan_df = daily_plan_df[daily_plan_df['db_name'] == db]
            get_log_details(daily_plan_df=db_daily_plan_df, db=db, node_mapper_list=node_mapper_list)
            node_mapper[db] = node_mapper_list
        for key, val in node_mapper.items():
            manifest_df = pd.DataFrame(val, columns=['job_name', 'bus_dt', 'slice_id', 'status', 'expected_dep',
                                                     'actual_dep', 'db_name', 'active', 'expected_start_time'])
            manifest_df_dict[key] = manifest_df
        return manifest_df_dict
    except Exception as e:
        log.exception("deployment.start_of_day_run.generate_log_details - Exception: %s", str(e))
        raise e

def main():
    """
    Main Function
    :param config:
    :return:
    """
    try:
        log.info("deployment.start_of_day_run.main - generate log details")
        parse_args(argv=sys.argv[1:])
        df_dict = generate_log_details()
        for key, df in df_dict.items():
            if key in CALC_DB_LIST:
                key = LQT_DB
                schema = LQT_SCHEMA
                table = LQT_JOB_LOG_TABLE
            elif key in SRC_DB_LIST:
                key = ARIP_DB
                schema = ARIP_SCHEMA
                table = ARI_JOB_LOG_TABLE
            else:
                continue  # ensure we don't add any garbage that other that what has been defined
            write_job_log_to_sf(df=df, db=key, schema=schema, table=table)
            log.info("deployment.start_of_day_run.main - Successfully inserted data log tables ")
    except Exception as e:
        log.exception("deployment.start_of_day_run.main - Exception: %s", str(e))
        raise e

if __name__ == "__main__":
    log.info("Initializing Start of day run to populate log tables from Daily plan")
    main()
else:
    parse_args(argv=sys.argv[1:])
