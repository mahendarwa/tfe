env_id_plain = executionenv if executionenv.upper() in ("DEV2", "DEV", "INT", "QA") else ""

final_sql = re.sub(r"\$\{env\.id\.upper\}", env_id.upper(), content)
final_sql = re.sub(r"\$\{env\.id\}", env_id_plain, final_sql)
