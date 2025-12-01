########################################
# 1. Postgres – IP based connection
########################################
psql -h 10.223.252.133 -p 5432 -U csgpgspl_user -d csgpgspl_db

########################################
# 2. Postgres – Hostname based (will fail if DNS not set)
########################################
psql -h psql-corp-use2-css-prod02.postgres.database.azure.com \
     -p 5432 -U csgpgspl_user -d csgpgspl_db

########################################
# 3. Tableau URL check
########################################
curl -I https://mytableau.cvs.com

########################################
# 4. SharePoint / O365 check
########################################
curl -I https://mytableau.cvs.com
# (same network path used – no direct SharePoint endpoint to curl)

########################################
# 5. SMTP relay connectivity
########################################
nc -vz smtptri.corp.cvsCaremark.com 25
# or
telnet smtptri.corp.cvsCaremark.com 25

########################################
# 6. Azure Blob endpoint test
########################################
curl -I https://strd1dbw0101csedev01.blob.core.windows.net

########################################
# 7. GCP host connectivity
########################################
ping -c 3 10.158.93.34
nc -vz 10.158.93.34 22   # SSH

########################################
# 8. AWS host connectivity
########################################
ping -c 3 10.173.21.12
nc -vz 10.173.21.12 22

ping -c 3 10.173.21.15
nc -vz 10.173.21.15 22

########################################
# 9. Wiz Cloud (only outbound check)
########################################
curl -I https://api.app.wiz.io

########################################
# 10. AppOmni connectivity
########################################
curl -I https://api.appomni.com

########################################
# 11. Git connectivity (replace <repo>)
########################################
git ls-remote https://github.com/<org>/<repo>.git

########################################
# 12. Python API check (generic)
########################################
python3 - << 'EOF'
import requests
print(requests.get("https://google.com").status_code)
EOF
