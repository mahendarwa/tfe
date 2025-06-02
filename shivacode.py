import re
sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), sql)
sql = re.sub(r"\$\{env\.id\.lower\}", env_id.lower(), sql)
sql = re.sub(r"\$\{env\.id\}", env_id, sql)
