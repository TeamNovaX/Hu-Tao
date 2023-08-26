#MIT License
#Copyright (c) 2023, ©NovaNetworks

import sys
from logging import getLogger

LOGGER = getLogger(__name__)

# Required ENV
try:
    BOT_TOKEN = ""
    API_ID = 123 #API ID
    API_HASH = ""
except Exception as e:
    LOGGER.error(f"Looks Like Something Is Missing!! Please Check Variables\n{e}")
    sys.exit(1)


TIMEZONE = "Asia/Kolkata"

COMMAND_HANDLER = ". /".split()

SUDO = list({int(x)for x in ("").split()})

SUPPORT_CHAT = "NovaSupports"

LOG_CHANNEL = "Weebs_Arena"

LOG_CHANNEL_ID = -1001954310607 #LOG GROUP ID FOR YOUR BOT

OWNER = list({int(x)for x in ("6149191605").split()}) #OWNER ID

DB_URL = ""

SQL_URL = ""

LEXICA_API = "https://lexica.qewertyy.me"