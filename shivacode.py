  env:
    TIME_ZONE: ${{ inputs.time_zone }}
timezone = os.getenv("TIME_ZONE", "CST") 


if timezone.upper() == "EST":
    set_timezone = "SET TIME ZONE 'america eastern';"
else:
    set_timezone = "SET TIME ZONE 'america central';"


bteq_content = f"""
.LOGON {host}/{user},Rp$QC$c_4dw;
{set_timezone}
COMPILE FILE = {temp_proc_path};
.LOGOFF;
.QUIT;
"""
