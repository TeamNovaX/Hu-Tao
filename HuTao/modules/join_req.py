#MIT License
#Copyright (c) 2023, ©NovaNetworks

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.enums import *

from HuTao import app, OWNER
from HuTao.Config import COMMAND_HANDLER
from HuTao.database.joinreq_db import *
from HuTao.helpers import *


@app.on_chat_join_request()
async def chat_join_req(_, message:Message):
    user = message.from_user
    chat = message.chat
    status = await jreq.find_one({"chat_id" : chat.id})

    if user.id in OWNER:
        try:
            await app.approve_chat_join_request(chat.id, user.id)
            await app.send_photo(
                chat.id,
                photo="https://graph.org//file/7ad7e0f73de5743262069.png",
                caption="{} was approved to join {}".format(user.mention, chat.title or "this chat")
            )
            return
        except:
            pass

    if not status:
      return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            "✅ Approve", callback_data="cb_approve#{}".format(user.id)
                    ),
                    InlineKeyboardButton(
                            "❌ Decline", callback_data="cb_decline#{}".format(user.id)
                    ),
                ]
            ]
    )
    await app.send_photo(
            chat.id,
            photo="https://graph.org//file/7ad7e0f73de5743262069.png",
            caption="{} wants to join {}".format(user.mention, chat.title or "this chat"),
            reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("cb_approve#"))
async def approve_join_req(_, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat
    try:
      userstatus = await app.get_chat_member(chat.id, user.id)
    except Exception as e:
       print(str(e))
    ok, user_id = cq.data.split("#")
    if userstatus:
     try:
      if userstatus.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        try:
          await app.approve_chat_join_request(chat.id, int(user_id))
          joined_user = await app.get_users(int(user_id))
          joined_mention = joined_user.mention
          admin_mention = user.mention
          await cq.message.edit_caption(
                f"{joined_mention}'s join request was approved by {admin_mention}.")
        
        except Exception as e:
          await cq.message.edit_caption(str(e))
          await cq.message.delete()
          print(str(e))
     except Exception as e:
       print(str(e))

@app.on_callback_query(filters.regex("cb_decline#"), group=-1)
async def decline_join_req(_, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat
    userstatus = await app.get_chat_member(chat.id, user.id)
    ok, user_id = cq.data.split("#")
    if userstatus:
     try:
      if userstatus.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        try:
          await app.decline_chat_join_request(chat.id, int(user_id))
          joined_user = await app.get_users(int(user_id))
          joined_mention = joined_user.mention
          admin_mention = user.mention
          await cq.message.edit_caption(
                f"{joined_mention}'s join request was declined by {admin_mention}.")
        
        except Exception as e:
          await cq.message.edit_caption(str(e))
          await cq.message.delete()
          print(e)
      else:
         await cq.answer("YOU CANT USE THIS!", True)
     except Exception:
       print(Exception)
    


@app.on_message(filters.command(["joinreq"], COMMAND_HANDLER))
@bot_admin
@user_admin
async def set_requests(_, message):
    chat = message.chat
    if len(message.command) == 1:
      return await message.reply_text("Usage: /joinreq on/off")
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    status = await jreq.find_one({"chat_id" : chat.id})
    if state == "on":
      if status:
         return await message.reply(f"Join Requests Alreday Enabled In {chat.title}")
      elif not status:
         await add_join(chat.id)
         await message.reply("Enabled join request menu in {}\nI will send a button menu to approve/decline new requests".format(chat.title))
    elif state == "off":
      if not status:
         return await message.reply(f"Join Requests Alreday Disabled In {chat.title}")
      elif status:
        await rm_join(chat.id)
        await message.reply("Disabled join request menu in {}\nI will no longer send a button menu to approve/decline new requests".format(chat.title))
