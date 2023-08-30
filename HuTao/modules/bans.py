import asyncio
from pyrogram.errors import ChatAdminRequired, RightForbidden, RPCError, PeerIdInvalid, UserAdminInvalid, UserNotParticipant
from pyrogram import filters
from pyrogram.types import CallbackQuery, ChatPrivileges, ChatPermissions,InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus

from HuTao import OWNER, BOT_ID, app, COMMAND_HANDLER
from HuTao.helpers.cache import ADMIN_CACHE, admin_cache_reload
from HuTao.helpers.status import *
from HuTao.helpers.extraction import extract_user
from HuTao.helpers.parser import mention_html
from HuTao.helpers.string import extract_time

@app.on_message(filters.command(["tban", "dtban", "stban"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def tban_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text(text="I can't ban nothing!")
        await message.stop_propagation()

    try:
        user_id, user_first_name, _ = await extract_user(c, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to ban")
        return
    if user_id == BOT_ID:
        await message.reply_text("Why would I ban myself?")
        await message.stop_propagation()

    if user_id in OWNER:
        await message.reply_text("I Cant Ban My Owner")
        await message.stop_propagation()

    r_id = message.reply_to_message.id if message.reply_to_message else message.id

    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        await message.reply_text("Read /help For Usage!!")
        return

    if not reason:
        await message.reply_text("You haven't specified a time to ban this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(message, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "ban")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot ban them!")
        await message.stop_propagation()

    if message.command[0] == "tban":
      try:
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        banned = await mention_html("USER", user_id)

        await message.chat.ban_member(
            user_id,
            until_date=bantime)
        t_t=f"""
**ACTION: T - BAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
BANNED USER: {banned}\n
""",
        txt = t_t
        if type(t_t) is tuple:
            txt = t_t[0]
        if reason:
          txt += f"REASON: {reason}\n"
        else:
          txt += "REASON: Not Specified\n"
        if time_val:
            txt += f"BANNED FOR:{time_val}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNBAN",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                reply_to_message_id=r_id,
                photo="https://graph.org//file/363c18fb1162093120ea4.jpg",
                caption=txt,
                reply_markup=keyboard
            )
        except Exception:
            await message.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard
            )
      except PeerIdInvalid:
          await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",)
      except UserNotParticipant:
          await message.reply_text("How can I Ban a user who is not a part of this chat?")
      except UserAdminInvalid:
          await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return
      
    if message.command[0] == "stban":
      try:
        await message.chat.ban_member(user_id, until_date=bantime)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
            return
        return
 
      except PeerIdInvalid:
          await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",)
      except UserNotParticipant:
          await message.reply_text("How can I Ban a user who is not a part of this chat?")
      except UserAdminInvalid:
          await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return
      
    if message.command[0] == "dtban":
      try:
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        banned = await mention_html("USER", user_id)
        await message.reply_to_message.delete()
        await message.chat.ban_member(
            user_id,
            until_date=bantime)
        t_t=f"""
**ACTION: DT - BAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
BANNED USER: {banned}\n
""",
        txt = t_t
        if type(t_t) is tuple:
            txt = t_t[0]
        if reason:
          txt += f"REASON: {reason}\n"
        else:
          txt += "REASON: Not Specified\n"
        if time_val:
            txt += f"BANNED FOR:{time_val}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNBAN",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                reply_to_message_id=r_id,
                photo="https://graph.org//file/363c18fb1162093120ea4.jpg",
                caption=txt,
                reply_markup=keyboard
            )
        except Exception:
            await message.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard
            )
      except PeerIdInvalid:
          await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",)
      except UserNotParticipant:
          await message.reply_text("How can I Ban a user who is not a part of this chat?")
      except UserAdminInvalid:
          await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return


@app.on_message(filters.command(["kick", "dkick", "skick"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def kick_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text(text="I can't kick nothing!")
        return

    if message.reply_to_message:
        r_id = message.reply_to_message.id
    else:
        r_id = message.id
    try:
        user_id, user_first_name, _ = await extract_user(c, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to kick")
        return

    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I kick myself?")
        await message.stop_propagation()

    if user_id in OWNER:
        await message.reply_text("Cannot Restrict My Owner")
        await message.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "kick")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot kick them!")
        await message.stop_propagation()
    if message.command[0] == "kick":
      try:
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        kicked = await mention_html("USER", user_id)
        await message.chat.ban_member(user_id)
        txt = f"""
**ACTION: KICK
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
KICKED USER: {kicked}
➖➖➖➖➖➖➖➖➖➖➖➖➖
"""
        try:
            await message.reply_photo(
                reply_to_message_id=r_id,
                photo="https://graph.org//file/363c18fb1162093120ea4.jpg",
                caption=txt
            )
        except:
            await message.reply_text(
                reply_to_message_id=r_id,
                text=txt
            )
        await message.chat.unban_member(user_id)
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",)
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,<b>Error:</b> <code>{ef}</code>""")
      return
    
    if message.command[0] == "skick":
      try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await message.chat.unban_member(user_id)
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?")
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured, Error: <code>{ef}</code>"""
        )
      return
    
    if message.command[0] == "dkick":
      try:
        await message.reply_to_message.delete()
        await message.chat.ban_member(user_id)
        admin = await mention_html(message.from_user.first_name, message.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        txt = f"""
**ACTION: D - KICK
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
KICKED USER: {kicked}
➖➖➖➖➖➖➖➖➖➖➖➖➖
"""
        try:
            await message.reply_photo(
                photo="https://graph.org//file/363c18fb1162093120ea4.jpg",
                caption=txt
            )
        except:
            await message.reply_text(txt)
        await message.chat.unban_member(user_id)
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?")
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
      return


@app.on_message(filters.command("unban", COMMAND_HANDLER))
@bot_admin
@user_admin
@bot_can_ban
@user_can_ban
async def unban_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text(text="I can't unban nothing!")
        await message.stop_propagation()

    if message.reply_to_message and not message.reply_to_message.from_user:
        user_id, user_first_name = (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(c, message)
        except Exception:
            return

    try:
        statu = (await message.chat.get_member(user_id)).status
        if statu not in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            await message.reply_text("User is not banned in this chat\nOr using this command as reply to his message")
            return
    except Exception as e:
       pass
    try:
        await message.chat.unban_member(user_id)
        admin = message.from_user.mention
        unbanned = await mention_html("USER", user_id)
        txt = f"""
**ACTION: UNBAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {admin}
UNBANNED USER: {unbanned}
➖➖➖➖➖➖➖➖➖➖➖➖➖**
"""
        await message.reply_text(txt)
    except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
    return


@app.on_message(filters.command(["ban", "sban", "dban"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def ban_usr(c: app, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text(text="I can't ban nothing!")
        await message.stop_propagation()

    if message.reply_to_message and not message.reply_to_message.from_user:
        user_id, user_first_name = (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(c, message)
        except Exception:
            return

    if not user_id:
        await message.reply_text("Cannot find user to ban")
        return
    if user_id == BOT_ID:
        await message.reply_text("Why would I ban myself?")
        await message.stop_propagation()

    if user_id in OWNER:
        await message.reply_text("I Cant Ban My Owner")
        await message.stop_propagation()

    if user_id == message.chat.id:
        await message.reply_text("That's an admin!")
        await message.stop_propagation()
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "ban")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot ban them!")
        await message.stop_propagation()

    reason = None
    if message.reply_to_message:
        r_id = message.reply_to_message.id
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
    else:
        r_id = message.id
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]

    if message.command[0] == "ban":
      try:
        await message.chat.ban_member(user_id)
        banned = await mention_html(user_first_name, user_id)
        txt = f"""
**ACTION: BAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {message.from_user.mention}
BANNED USER: {banned}\n
"""
        if reason:
          txt += f"REASON: {reason}\n"
        else:
          txt += "REASON: Not Specified\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNBAN",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await message.reply_photo(
                reply_to_message_id=r_id,
                photo="https://graph.org//file/87a24439448fd8e6a0ba4.png",
                caption=txt,
                reply_markup=keyboard
            )
        except Exception:
            
            await message.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard
            )
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?")
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
      return
      
    if message.command[0] == "sban":
      try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?")
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
      return
    
    if message.command[0] == "dban":
      try:
        await message.reply_to_message.delete()
        await message.chat.ban_member(user_id)
        txt = f"""
**ACTION: BAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {message.from_user.mention}
BANNED USER: {banned}\n
"""
        if reason:
          txt += f"REASON: {reason}\n"
        else:
          txt += "REASON: Not Specified\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "UNBAN",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        try:
            await c.send_photo(
                message.chat.id, photo="https://graph.org//file/363c18fb1162093120ea4.jpg", caption=txt, reply_markup=keyboard
            )
        except Exception:
            await c.send_message(message.chat.id, txt ,reply_markup=keyboard)

      except ChatAdminRequired:
        await message.reply_text(text="I'message not admin or I don't have rights.")
      except PeerIdInvalid:
        await message.reply_text("I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?")
      except UserAdminInvalid:
        await message.reply_text("Cannot act on this user, maybe I wasn't the one who changed their permissions.")
      except RPCError as ef:
        await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
      return

@app.on_callback_query(filters.regex("^unban_"))
async def unbanbutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unban_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user:
        await q.answer(
            "You don't have enough permission to do this!",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and q.from_user.id != OWNER:
        await q.answer(
            "You don't have enough permission to do this!",
            show_alert=True,
        )
        return
    whoo = await c.get_chat(user_id)
    doneto = whoo.first_name if whoo.first_name else whoo.title
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    await q.message.edit_text(f"""
**ACTION: UNBAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
ADMIN: {q.from_user.mention}

UNBANNED USER: {doneto}
➖➖➖➖➖➖➖➖➖➖➖➖➖**
""")
    return


@app.on_message(filters.command("kickme", COMMAND_HANDLER))
@bot_admin
@bot_can_ban
async def kickme(c: app, message: Message):
    reason = None
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    try:
        mem = await c.get_chat_member(message.chat.id, message.from_user.id)
        if mem.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                await c.promote_chat_member(
                    message.chat.id,
                    message.from_user.id,
                    ChatPrivileges(can_manage_chat=False)
                )
            except Exception:
                await message.reply_text("I can't demote you so I can't ban you")
                return
        await message.chat.ban_member(message.from_user.id)
        txt = f"""
**ACTION: KICK ME
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {message.from_user.mention}\n
"""
        if reason:
          txt += f"REASON: {reason}\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        else:
          txt += "REASON: Not Specified\n➖➖➖➖➖➖➖➖➖➖➖➖➖**"
        a = await message.reply_photo("https://graph.org//file/f207b657444d0ad67794d.png", caption=txt)
        await message.chat.unban_member(message.from_user.id)
        asyncio.sleep(5)
        await a.delete()
    except RPCError as ef:
        if "400 USER_ADMIN_INVALID" in ef:
            await message.reply_text("Looks like I can't kick you")
            return
        else:
            await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
    except Exception as ef:
          await message.reply_text(f"""Some error occured,\nError: <code>{ef}</code>""")
          return


# __PLUGIN__ = "bans"

# _DISABLE_CMDS_ = ["kickme"]

# __alt_name__ = [
#     "ban",
#     "unban",
#     "kickme",
#     "kick",
#     "tban",
# ]

# __HELP__ = """
# **Bans**

# **Admin only:**
# • /kick: Kick the user replied or tagged.
# • /skick: Kick the user replied or tagged and delete your messsage.
# • /dkick: Kick the user replied and delete their message.
# • /ban: Bans the user replied to or tagged.
# • /sban: Bans the user replied or tagged and delete your messsage.
# • /dban: Bans the user replied and delete their message.
# • /tban <userhandle> x(message/h/d): Bans a user for x time. (via handle, or reply). message = minutes, h = hours, d = days.
# • /stban <userhandle> x(message/h/d): Silently bans a user for x time. (via handle, or reply). message = minutes, h = hours, d = days.
# • /dtban <userhandle> x(message/h/d): Silently bans a user for x time and delete the replied message. (via reply). message = minutes, h = hours, d = days.
# • /unban: Unbans the user replied to or tagged.

# **Example:**
# `/ban @username`: this bans a user in the chat."""
