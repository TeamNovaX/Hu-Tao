#MIT License
#Copyright (c) 2023, ©NovaNetworks

import time
from logging import ERROR, INFO, StreamHandler, basicConfig, getLogger, handlers
from pyrogram import Client

from HuTao.Config import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    TIMEZONE,
    LOG_CHANNEL,
    SUDO,
    DB_URL,
    LOG_CHANNEL_ID,
    OWNER,
    SQL_URL,
    LEXICA_API,
    COMMAND_HANDLER
)

#LOGGER SETUP
basicConfig(
    level=INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s.%(funcName)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        handlers.RotatingFileHandler("HuTaoLogs.txt", mode="w+", maxBytes=1000000),
        StreamHandler(),
    ],
)
getLogger("pyrogram").setLevel(ERROR)


# --------------------------------- #

MOD_LOAD = []
MOD_NOLOAD = []
HELPABLE = {}
start = time.time()
Hutao_Ver = "0.0.1"

# --------------------------------- #

# SET UP THE CLIENT
app = Client(
    "HuTao",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START THE CLIENT AND GET INFO
app.start()
BOT_ID = app.me.id
BOT_NAME = app.me.first_name
BOT_USERNAME = app.me.username