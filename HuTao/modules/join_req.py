import re
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from HuTao import app, SUDO
from HuTao.helpers import *


@app.on_chat_join_request()
async def chat_join_req(_, message:Message):
    user = message.from_user
    chat = message.chat

    if user.id in SUDO:
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

    # if not join_req_status(chat.id):
    #     return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            "✅ Approve", callback_data="cb_approve={}".format(user.id)
                    ),
                    InlineKeyboardButton(
                            "❌ Decline", callback_data="cb_decline={}".format(user.id)
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


@app.on_callback_query(filters.regex("cb_approve="))
async def approve_join_req(_, cq: CallbackQuery) -> str:
    user = cq.from_user
    chat = cq.message.chat
    try:
      userstatus = await app.get_chat_member(chat.id, user.id) 
    except Exception:
       pass
    match = re.match(r"cb_approve=(.+)", cq.data)

    user_id = match.group(1)
    try:
      if (userstatus.status in COMMANDERS) and user.id in SUDO:
        try:
          await app.approve_chat_join_request(chat.id, user_id)
          joined_user = await app.get_users(user_id)
          joined_mention = joined_user.mention
          admin_mention = user.mention
          await cq.message.edit_caption(
                f"{joined_mention}'s join request was approved by {admin_mention}.")
        
        except Exception as e:
          await cq.message.edit_caption(str(e))
          await cq.message.delete()
          pass
    except Exception:
       pass

@app.on_callback_query(filters.regex("cb_decline="))
async def decline_join_req(_, cq: CallbackQuery) -> str:
    user = cq.from_user
    chat = cq.message.chat
    try:
      userstatus = await app.get_chat_member(chat.id, user.id) 
    except Exception:
       pass
    match = re.match(r"cb_decline=(.+)", cq.data)

    user_id = match.group(1)
    try:
      if (userstatus.status in COMMANDERS) and user.id in SUDO:
        try:
          await app.decline_chat_join_request(chat.id, user_id)
          joined_user = await app.get_users(user_id)
          joined_mention = joined_user.mention
          admin_mention = user.mention
          await cq.message.edit_caption(
                f"{joined_mention}'s join request was declined by {admin_mention}.")
        
        except Exception as e:
          await cq.message.edit_caption(str(e))
          await cq.message.delete()
          pass
    except Exception:
       pass