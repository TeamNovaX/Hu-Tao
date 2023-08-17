#MIT License
#Copyright (c) 2023, ©NovaNetworks


import asyncio
import importlib
import os
import pickle
import traceback
from logging import getLogger

from pyrogram import __version__, idle
from pyrogram.raw.all import layer

from HuTao import LOG_CHANNEL, BOT_USERNAME, HELPABLE, app
from HuTao.modules import ALL_MODULES
from HuTao.Config import SUDO

LOGGER = getLogger(__name__)
loop = asyncio.get_event_loop()


# Run Bot
async def start_bot():
    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"HuTao.modules.{module}")
        if hasattr(imported_module, "__mod__") and imported_module.__mod__:
            imported_module.__mod__ = imported_module.__mod__
            if hasattr(imported_module, "__help__") and imported_module.__help__:
                HELPABLE[imported_module.__mod__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "| {:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "| {:<15}".format(i)
        j += 1
    
    LOGGER.info(bot_modules)
    LOGGER.info("[INFO]: BOT STARTED: @%s!", BOT_USERNAME)

    try:
        LOGGER.info("[INFO]: START MESSAGE")
        await app.send_message(LOG_CHANNEL, f"BOT STARTED")
    except Exception as e:
        LOGGER.error(str(e))
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception:
        err = traceback.format_exc()
        LOGGER.info(err)
    finally:
        loop.stop()
        LOGGER.info(
            "------------------------ Stopped Services ------------------------"
        )