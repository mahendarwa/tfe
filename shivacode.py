bteq <<EOF
.logon HSTNTDPROD.HealthSpring.Inside/AUTOCHG_USER_CHS_PRD
$_bdgE7r1#Tr
.run file=final_script.sql;
.logoff;
.quit;
EOF
