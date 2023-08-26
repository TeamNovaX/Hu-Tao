# Copyright 2023 Qewertyy, MIT License

import os
from HuTao import app
from HuTao.Config import COMMAND_HANDLER
from HuTao.helper import getFile,UpscaleImages

@app.on_message(filters.command("upscale", COMMAND_HANDLER))
async def upscaleImages(_,message):
    file = await getFile(message)
    if fileId is None:
        return await message.reply_text("Replay to an image?")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    await message.send_document(message.chat.id,open(upscaledImage,"rb"))
    os.remove(upscaledImage)