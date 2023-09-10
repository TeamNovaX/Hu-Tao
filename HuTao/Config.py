#MIT License
#Copyright (c) 2023, ©NovaNetworks

import sys
from logging import getLogger

LOGGER = getLogger(__name__)

# Required ENV
try:
    BOT_TOKEN = "6545120508:AAEfQ4_q4u4O91wbenxwJwFxpNnJPsiclo8" # BOT TOKEN
    API_ID =  21213662 # API ID
    API_HASH = "64ffedbdbf1fe4fad73ecc548e5f31e0" # API HASH
except Exception as e:
    LOGGER.error(f"Looks Like Something Is Missing!! Please Check Variables\n{e}")
    sys.exit(1)


TIMEZONE = "Asia/Kolkata" # YOUR TIME ZONE

COMMAND_HANDLER = ". /".split() # COMMAND HANDLER

SUDO = list({int(x)for x in ("").split()})

SUPPORT_CHAT = "NovaSupports" # SUPPORT GROUP (ID OR USERNAME)

LOG_CHANNEL_ID = -1001816188874 #LOG GROUP ID FOR YOUR BOT

OWNER = list({int(x)for x in ("5565211830").split()}) #OWNER ID

DB_URL = "mongodb+srv://k03858372:6K2rjELO324mcoLk@testing.qryiptk.mongodb.net/?retryWrites=true&w=majority" # MONGO DB URL

SQL_URL = "postgresql://giievlqx:mcgUjVmxBnQOoJHC21RxKUDNhUwenmBv@rogue.db.elephantsql.com/giievlqx" # ELEPHANT SQL URL