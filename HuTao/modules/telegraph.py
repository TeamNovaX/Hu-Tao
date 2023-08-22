import os
from pyrogram import filters
from telegraph import upload_file
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from HuTao import app
from HuTao.Config import COMMAND_HANDLER


@app.on_message(filters.command("tgm", COMMAND_HANDLER))
async def gentelegraph(_, message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("Reply To Some Media")
    if reply.media:
      try:
          i = await message.reply("Generating Telegraph Link....")
          path = await reply.download()
          fk = upload_file(path)
          for x in fk:
              url = "https://graph.org/" + x

          await i.edit(f'**Your Telegraph Link Is Generated** [🎉]({url})', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Telegraph", url =f"{url}"), InlineKeyboardButton ("Share", url=f"https://telegram.me/share/url?url={url}")]]))
          os.remove(path)
      except Exception as e:
          await i.edit(f"ERROR: **{e}**")
          os.remove(path)