import asyncio
from HuTao.database.users_db import *
from HuTao import app, OWNER
from pyrogram import filters

@app.on_message(filters.command("pcast") & filters.user(OWNER), group=-50)
async def broadcast(_, message):
    if message.reply_to_message:
      to_send=message.reply_to_message.id
    if not message.reply_to_message:
      return await message.reply_text("Reply To Some Post To Broadcast")
    chats = await get_all_chat_ids() or []
    users = await get_all_user_ids() or []
    print(chats)
    print(users)
    failed = 0
    for chat in chats:
      try:
        await app.forward_messages(chat_id=int(chat), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception:
        failed += 1
    
    failed_user = 0
    for user in users:
      try:
        await app.forward_messages(chat_id=int(user), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception as e:
        failed_user += 1


    await message.reply_text("Broadcast complete. {} groups failed to receive the message, probably due to being kicked. {} users failed to receive the message, probably due to being banned.".format(failed, failed_user))
