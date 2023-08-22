#MIT License
#Copyright (c) 2023, ©NovaNetworks

import sys
from logging import getLogger

LOGGER = getLogger(__name__)

# Required ENV
try:
    BOT_TOKEN = "6601317680:AAFYMO0cofvQvxtY3K-AKYDDVBvxyuvtEuE"
    API_ID =  10582318
    API_HASH = "ae5cb28621683b35873d9f71e7279471"
except Exception as e:
    LOGGER.error(f"Looks Like Something Is Missing!! Please Check Variables\n{e}")
    sys.exit(1)


TIMEZONE = "Asia/Kolkata"

COMMAND_HANDLER = ". /".split()

SUDO = list({int(x)for x in ("").split()})

SUPPORT_CHAT = "NovaSupports"

LOG_CHANNEL = "Weebs_Arena"

LOG_CHANNEL_ID = -1001956854737

OWNER = list({int(x)for x in ("6149191605").split()})

DB_URL = "mongodb+srv://kirito1240:kito@hutao.bm9yhnj.mongodb.net/?retryWrites=true&w=majority"

