env_id = os.getenv("ENV_ID", "DEV")
sql = sql.replace("${env.id.upper}", env_id.upper())
sql = sql.replace("${env.id.lower}", env_id.lower())
