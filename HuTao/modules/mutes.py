from pyrogram import enums
from pyrogram.errors import ChatAdminRequired, RightForbidden, RPCError, UserNotParticipant
from pyrogram import filters
from pyrogram.types import CallbackQuery, ChatPermissions,InlineKeyboardButton, InlineKeyboardMarkup

from HuTao import OWNER, BOT_ID, app, COMMAND_HANDLER
from HuTao.helpers.cache import ADMIN_CACHE, admin_cache_reload
from HuTao.helpers.status import *
from HuTao.helpers.extraction import extract_user
from HuTao.helpers.parser import mention_html
from HuTao.helpers.string import extract_time


@app.on_message(filters.command(["tmute", "dtmute", "stmute"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def tmute_usr(c: app, message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("Give A ID or Reply To A User To Mute!")
        return

    try:
        user_id, user_first_name, _ = await extract_user(c, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("You don't seem to be referring to a user or the ID specified is incorrect..")
        return
    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I mute myself?")
        return

    if user_id in OWNER:
        await message.reply_text("This Is My Owner I Cant Restrict Him")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot mute them!")
        return

    r_id = message.reply_to_message.id if message.reply_to_message else message.id

    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        await message.reply_text("Read /help For Usage!!")
        return

    if not reason:
        await message.reply_text("You haven't specified a time to mute this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    mutetime = await extract_time(message, time_val)

    if not mutetime:
        return
    if message.command[0] == "tmute":
      try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        muted = await mention_html("USER", user_id)
        txt = f"""
**ACTION: T - MUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {muted}
BY ADMIN: {admin}\n
"""
        if reason:
            txt += f"REASON: {reason}\n"
        else:
            txt += "REASON: Not Specified\n"
        if mutetime:
            txt += f"MUTED FOR: {time_val}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNMUTE",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                photo="https://graph.org//file/ad02d4190326d04c39a91.jpg",
                caption=txt,
                reply_markup=keyboard,
                reply_to_message_id=r_id,
            )
        except Exception:
            await message.reply_text(txt,reply_markup=keyboard, reply_to_message_id=r_id)

      except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
      except RPCError as ef:
        await message.reply_text(
            text=f"""Some error occured,\nError: <code>{ef}</code>""")
      return
    if message.command[0] == "dtmute":
        if not message.reply_to_message:
           return await message.reply_text("No replied message and user to delete and mute!")
        
        await message.reply_to_message.delete()

        try:
          await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
          admin = await mention_html(message.from_user.first_name, message.from_user.id)
          muted = await mention_html("USER", user_id)
          txt = f"""
**ACTION: D - MUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {muted}
BY ADMIN: {admin}\n
"""
          if reason:
            txt += f"REASON: {reason}\n"
          else:
            txt += "REASON: Not Specified\n"
          if mutetime:
            txt += f"MUTED FOR: {time_val}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
          keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNMUTE",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )

          try:
            await message.reply_photo(
                photo="https://graph.org//file/ad02d4190326d04c39a91.jpg",
                caption=txt,
                reply_markup=keyboard,
            )
          except Exception:
            await message.reply_text(txt,reply_markup=keyboard)
        except UserNotParticipant:
          await message.reply_text("How can I mute a user who is not a part of this chat?")
        except RPCError as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return

    if message.command[0] == "stmute":
        try:
          await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
          
          await message.delete()

          if message.reply_to_message:
            await message.reply_to_message.delete()
        
        except UserNotParticipant:
          await message.reply_text("How can I mute a user who is not a part of this chat?")
        except RPCError as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return



@app.on_message(filters.command(["mute", "dmute", "smute"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def mute_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("Give A ID or Reply To A User To Mute!")
        return

    reason = None
    if message.reply_to_message:
        r_id = message.reply_to_message.id
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
    else:
        r_id = message.id
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]
    try:
        user_id, user_first_name, _ = await extract_user(c, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Give A ID or Reply To A User To Mute!")
        return
    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I mute myself?")
        return

    if user_id in OWNER:
        await message.reply_text("This Is My Owner I Cant Restrict Him")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot mute them!")
        return
    
    if message.command[0] == "mute":
      try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        muted = await mention_html("USER", user_id)
        txt = f"""
**ACTION: MUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {muted}
BY ADMIN: {admin}\n
"""
        if reason:
          txt += f"REASON: {reason}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        else:
          txt += "REASON: Not Specified\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNMUTE",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                photo="https://graph.org//file/ad02d4190326d04c39a91.jpg",
                caption=txt,
                reply_markup=keyboard,
                reply_to_message_id=r_id,
            )
        except Exception:
            await message.reply_text(txt,reply_markup=keyboard, reply_to_message_id=r_id)
      except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
        return
      
    if message.command[0] == "smute":
      try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )
        
        await message.delete()

        if message.reply_to_message:
            await message.reply_to_message.delete()
            return
        return
      except UserNotParticipant:
         await message.reply_text("How can I mute a user who is not a part of this chat?")
      except RPCError as ef:
         await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
         return
    if message.command[0] == "dmute":
      try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )

        await message.reply_to_message.delete()

        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        muted = await mention_html("USER", user_id)

        txt = f"""
**ACTION: D - MUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {muted}
BY ADMIN: {admin}\n
"""
        if reason:
          txt += f"REASON: {reason}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        else:
          txt += "REASON: Not Specified\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNMUTE",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                photo="https://graph.org//file/ad02d4190326d04c39a91.jpg",
                caption=txt,
                reply_markup=keyboard,
            )
        except Exception:
            await message.reply_text(txt,reply_markup=keyboard)
      except UserNotParticipant:
         await message.reply_text("How can I mute a user who is not a part of this chat?")
      except RPCError as ef:
         await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
         return


@app.on_message(filters.command("unmute", COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def unmute_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't unmute nothing!")
        return

    try:
        user_id, user_first_name, _ = await extract_user(c, message)
    except Exception:
        return

    if user_id == BOT_ID:
        await message.reply_text("Does It Make Any Sense?")
        return
    try:
        statu = (await message.chat.get_member(user_id)).status
        if statu not in [enums.ChatMemberStatus.BANNED,enums.ChatMemberStatus.RESTRICTED]:
            await message.reply_text("User is not muted in this chat\nOr using this command as reply to his message")
            return
    except Exception as e:
        pass
    try:
        await message.chat.unban_member(user_id)
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        unmuted = await mention_html("USER", user_id)
        await message.reply_text(text=f"""
**ACTION: UNMUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
UNMUTED USER: {unmuted}
➖➖➖➖➖➖➖➖➖➖➖➖➖**
""")
    except ChatAdminRequired:
        await message.reply_text(text="I'm not admin or I don't have rights.")
    except UserNotParticipant:
        await message.reply_text("How can I unmute a user who is not a part of this chat?")
    except RightForbidden:
        await message.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await message.reply_text(
            text=f"""Some error occured, Error: <code>{ef}</code>""")
    return


@app.on_callback_query(filters.regex("^unmute_"))
async def unmutebutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unmute_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user:
        await q.answer(
            "You don't have enough permission to do this!",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and user.id != OWNER:
        await q.answer(
            "You don't have enough permission to do this!",
            show_alert=True,
        )
        return
    whoo = await c.get_users(user_id)
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    await q.message.edit_text(f"""
**ACTION: UNMUTE
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {q.from_user.mention}

UNMUTED USER: {whoo.mention}
➖➖➖➖➖➖➖➖➖➖➖➖➖**
""")
    return




__mod__ = "MUTES"

__help__ = """
»**Admin only:**

» /mute: Mute the user replied to or mentioned.
» /smute: silences a user without notifying. Can also be used as a reply, muting the replied to user.
» /dmute: Mute a user by reply, and delete their message.
» /tmute <username> x(message/h/d): mutes a user for x time. (via username, or reply). m = minutes, h = hours, d = days.
» /stmute <username> x(m/h/d): mutes a user for x time without notifying. (via username, or reply). m = minutes, h = hours, d = days.
» /dtmute <username> x(m/h/d): Mute the replied user, and delete the replied message. (via reply). m = minutes, h = hours, d = days.
» /unmute: Unmutes the user mentioned or replied to.

»**Example:**
`/mute @username`: this mutes a user."""