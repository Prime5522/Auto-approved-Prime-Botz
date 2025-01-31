from os import environ

API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

AUTH_CHANNEL = int(environ.get("AUTH_CHANNEL", ""))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", ""))
ADMINS = int(environ.get("ADMINS", ""))

# Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_URI = environ.get("DB_URI", "")
DB_NAME = environ.get("DB_NAME", "Cluster0")

# If this is True Then Bot Accept New Join Request 
NEW_REQ_MODE = bool(environ.get('NEW_REQ_MODE', True))
