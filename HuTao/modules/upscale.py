# Copyright 2023 Qewertyy, MIT License

import os
from pyrogram import filters
from HuTao import app, BOT_USERNAME
from HuTao.Config import COMMAND_HANDLER
from HuTao.helpers import getFile, UpscaleImages

@app.on_message(filters.command("upscale", COMMAND_HANDLER))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("Replay to an image?")
    msg = await message.reply("Wait A Min.. Upscalling Your Image")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"), caption=f"Upscaled By @{BOT_USERNAME}")
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}")
