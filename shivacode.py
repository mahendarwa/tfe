# Set bteq_cmd based on execution environment
if executionenv.upper() == "UAT":
    bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},RpSQC\\$c_4dwv;
.run file=final_script.sql;
.logoff;
.quit;
EOF
"""
elif executionenv.upper() == "PRD":
    bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},T#4!@asd*&;
.run file=final_script.sql;
.logoff;
.quit;
EOF
"""
else:
    bteq_cmd = f"""
bteq <<EOF
.logon {host}/{user},{pwd};
.run file=final_script.sql;
.logoff;
.quit;
EOF
"""
