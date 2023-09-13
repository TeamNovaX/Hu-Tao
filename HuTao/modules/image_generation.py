# Copyright 2023 Qewertyy, MIT License

import os
from pyrogram import filters
from HuTao import app, BOT_USERNAME
from HuTao.Config import COMMAND_HANDLER
from HuTao.helpers import ImageGeneration, ImageModels, getText
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,InputMediaDocument

PromptDB = {}

@app.on_message(filters.command("draw", COMMAND_HANDLER))
async def generate(_, message):
    global PromptDB
    prompt = await getText(message)
    if prompt is None:
        return await message.reply_text("No prompt given")
    user = message.from_user
    btns = []
    PromptDB[user.id] = {'prompt':prompt,'reply_to_id':message.id}
    for i in ImageModels:
        btns.append(InlineKeyboardButton(text=i,callback_data=f"draw.{ImageModels[i]}.{user.id}"))
    btns = [[btns[0],btns[1]],[btns[2],btns[3]],[btns[4],btns[5]]]
    await message.reply_photo("https://graph.org//file/a24ad0babb868d539b744.jpg", caption=f"**SELECT A MODEL TO GENERATE**",reply_markup=InlineKeyboardMarkup(btns))

@app.on_callback_query(filters.regex("^draw.(.*)"))
async def draw(_,query):
    global PromptDB
    data = query.data.split('.')
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("Not Your Query!")
    promptdata = PromptDB.get(auth_user,None)
    if promptdata is None:
        return await query.edit_message_text("something went wrong report it at @NovaSupports")
    await query.edit_message_text("Please wait, generating your image")
    img_url = await ImageGeneration(int(data[1]),promptdata['prompt'])
    if img_url is None or img_url == 2 or img_url ==1:
        return await query.edit_message_text("something went wrong report it at @NovaSupports")
    images = []
    await query.message.delete()
    del PromptDB[auth_user]
    for i in img_url:
        images.append(InputMediaDocument(i, caption=f"YOUR PROMPT: {promptdata['prompt']}\n\nBY: @{BOT_USERNAME}"))

    await app.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptdata['reply_to_id']
    )
