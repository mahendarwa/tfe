import argparse, sys
import deployment.dbt_logger as dbt_logger
import deployment.snowflake_handler as sf_handler

log = dbt_logger.initialize(__name__)

sf_connection = None
sf_cursor = None
command = None
host_name = None

def parse_args(argv=None):
    """
    Parse command-line arguments to set global variables.
    """
    global command, host_name
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', help='Command to issue to the host (e.g., "shutdown")', type=str)
    parser.add_argument('--host_name', help='Name of the host to which the command will be issued', type=str)
    args = parser.parse_args(argv)
    command = args.command
    host_name = args.host_name

def issue_host_command(command, host_name):
    """
    Updates the HOST_COMMAND column in the DBT_HOSTS table for a specified host.
    """
    global sf_cursor, sf_connection
    try:
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
        log.exception("Error in issuing host command - Exception: %s", str(e))
        raise e

def main():
    """
    Main function to process command-line arguments and issue the specified host command.
    """
    log.info("Starting script to issue commands to hosts.")
    parse_args(argv=sys.argv[1:])
    if command and host_name:
        issue_host_command(command=command, host_name=host_name)
    else:
        log.info("No command or host name specified. Skipping command issuance.")

if __name__ == "__main__":
    log.info("Initializing Host Command Issuance Script")
    main()
python issue_host_command.py --command "shutdown" --host_name "example_host"
