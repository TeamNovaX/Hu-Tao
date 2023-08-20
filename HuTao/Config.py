#MIT License
#Copyright (c) 2023, ©NovaNetworks

import sys
from logging import getLogger

LOGGER = getLogger(__name__)

# Required ENV
try:
    BOT_TOKEN = "" #BOT TOKEN
    API_ID = 1234 #API ID (GET IT FROM my.telegram.org)
    API_HASH = "" #API HASH (GET IT FROM my.telegram.org)
except Exception as e:
    LOGGER.error(f"Looks Like Something Is Missing!! Please Check Variables\n{e}")
    sys.exit(1)


TIMEZONE = "Asia/Kolkata" #SET ACCORDING TO YOUR REGION

COMMAND_HANDLER = ". /".split()

SUDO = list({int(x)for x in ("").split()})

SUPPORT_CHAT = "NovaSupports" #SUPPORT GROUP FOR YOUR BOT

LOG_CHANNEL = "Weebs_Arena" #LOG GROUP FOR YOUR BOT

DB_URL = "" #MONGO DB LINK