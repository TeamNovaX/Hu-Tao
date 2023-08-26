from asyncio import sleep
import os

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType
from pyrogram.errors import (ChatAdminInviteRequired, ChatAdminRequired,
                             FloodWait, RightForbidden, RPCError,
                             UserAdminInvalid, BadRequest)
from pyrogram.types import ChatPrivileges, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from HuTao import app, OWNER
from HuTao.helpers.cache import (ADMIN_CACHE, TEMP_ADMIN_CACHE_BLOCK, admin_cache_reload)
from HuTao.helpers.status import *

from HuTao.helpers.extraction import extract_user
from HuTao.helpers.parser import mention_html
from HuTao.Config import COMMAND_HANDLER


@app.on_message(filters.command("adminlist", COMMAND_HANDLER))
async def adminlist_show(_, m: Message):
    global ADMIN_CACHE
    if m.chat.type not in [ChatType.SUPERGROUP,ChatType.GROUP]:
        return await m.reply_text(
            text="This command is made to be used in groups only!",
        )
    try:
        try:
            admin_list = ADMIN_CACHE[m.chat.id]
            note = "**Note: These are cached values!**"
        except KeyError:
            admin_list = await admin_cache_reload(m, "adminlist")
            note = "**Note: These are up-to-date values!**"
        adminstr = f"**ADMINS IN {m.chat.title}:**" + "\n\n"
        bot_admins = [i for i in admin_list if (i[1].lower()).endswith("bot")]
        user_admins = [i for i in admin_list if not (i[1].lower()).endswith("bot")]
        mention_users = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in user_admins
            if not admin[2] 
        ]
        mention_users.sort(key=lambda x: x[1])
        mention_bots = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in bot_admins
        ]
        mention_bots.sort(key=lambda x: x[1])
        adminstr += "<b>ADMINS:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_users)
        adminstr += "\n\n<b>BOTS:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_bots)
        await m.reply_text(adminstr + "\n\n" + note)
    except Exception as ef:
        if str(ef) == str(m.chat.id):
            await m.reply_text(text="Use /admincache to reload admins!")
        else:
            ef = str(ef) + f"{admin_list}\n"
            await m.reply_text(
                text=f"Some error occured, <b>Error:</b> <code>{ef}</code>"
            )
    return


@app.on_message(filters.command("zombies", COMMAND_HANDLER))
@user_can_ban
@bot_can_ban
@bot_admin
@user_admin
async def zombie_clean(c: app, m: Message):
    zombie = 0
    wait = await m.reply_text("Cleaning Up Zombies....")
    async for member in c.get_chat_members(m.chat.id):
        if member.user.is_deleted:
            zombie += 1
            try:
                await c.ban_chat_member(m.chat.id, member.user.id)
            except UserAdminInvalid:
                zombie -= 1
            except FloodWait as e:
                await sleep(e.x)
    if zombie == 0:
        return await wait.edit_text("Group is clean!")
    return await wait.edit_text(
        text=f"<b>{zombie}</b> Zombies found and has been banned!",
    )

@app.on_message(filters.command("admincache", COMMAND_HANDLER))
async def reload_admins(_, m: Message):
    global TEMP_ADMIN_CACHE_BLOCK
    if m.chat.type not in [ChatType.SUPERGROUP,ChatType.GROUP]:
        return await m.reply_text(
            "This command is made to be used in groups only!",
        )
    if (
        (m.chat.id in set(TEMP_ADMIN_CACHE_BLOCK.keys()))
        and (m.from_user.id not in OWNER)
        and TEMP_ADMIN_CACHE_BLOCK[m.chat.id] == "manualblock"
    ):
        await m.reply_text("Can only reload admin cache once per 10 mins!")
        return
    try:
        await admin_cache_reload(m, "admincache")
        TEMP_ADMIN_CACHE_BLOCK[m.chat.id] = "manualblock"
        await m.reply_text(text="Reloaded all admins in this chat!")
    except RPCError as ef:
        await m.reply_text(
            text=f"Some error occured, <b>Error:</b> <code>{ef}</code>"
        )
    return


@app.on_message(filters.command("promote", COMMAND_HANDLER))
@bot_admin
@bot_can_promote
@user_admin
@user_can_promote
async def promote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(
            text="You don't seem to be referring to a user or the ID specified is incorrect.."
        )
        return
    try:
        user_id, user_first_name, user_name = await extract_user(c, m)
    except Exception:
        return
    bot = await c.get_chat_member(m.chat.id, BOT_ID)
    if user_id == BOT_ID:
        await m.reply_text("Huh, how can I even promote myself?")
        return
    if not bot.privileges.can_promote_members:
        return await m.reply_text(
            "I don't have enough permissions",
        ) 
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "promote_cache_update"))
        }
    if user_id in admin_list:
        await m.reply_text(
            "This user is already an admin, how am I supposed to re-promote them?",
        )
        return
    try:
        await m.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.privileges.can_change_info,
                can_invite_users=bot.privileges.can_invite_users,
                can_delete_messages=bot.privileges.can_delete_messages,
                can_restrict_members=bot.privileges.can_restrict_members,
                can_pin_messages=bot.privileges.can_pin_messages,
                can_manage_chat=bot.privileges.can_manage_chat,
                can_manage_video_chats=bot.privileges.can_manage_video_chats,
            ),
        )
        title = ""
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            title = "Admin"  # Deafult title
            if len(m.text.split()) >= 3 and not m.reply_to_message:
                title = " ".join(m.text.split()[2:16]) # trim title to 16 characters
            elif len(m.text.split()) >= 2 and m.reply_to_message:
                title = " ".join(m.text.split()[1:16]) # trim title to 16 characters
            try:
                await c.set_administrator_title(m.chat.id, user_id, title)
            except RPCError as e:
                pass
            except Exception as e:
                pass
        keyboard= InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Low Promote",
                        callback_data=f"admin_lpromote_{user_id}_{m.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text="Full Promote",
                        callback_data=f"admin_fpromote_{user_id}_{m.from_user.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Demote",
                        callback_data=f"admin_demote_{user_id}_{m.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text="❌",
                        callback_data=f"admin_delete_{user_id}_{m.from_user.id}",
                    ),
                ],
            ],
        )
        await m.reply_text(f"""
<b>• EVENT: PROMOTION
➖➖➖➖➖➖➖➖➖➖➖➖
- ADMIN: {await mention_html(m.from_user.first_name, m.from_user.id)}
- USER: {await mention_html(user_first_name, user_id)}
➖➖➖➖➖➖➖➖➖➖➖➖</b>
""", reply_markup=keyboard
        )
        try:
            inp1 = user_name or user_first_name
            admins_group = ADMIN_CACHE[m.chat.id]
            admins_group.append((user_id, inp1))
            ADMIN_CACHE[m.chat.id] = admins_group
        except KeyError:
            await admin_cache_reload(m, "promote_key_error")
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to promote this user.")
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RPCError as e:
        await m.reply_text(
            text=f"Some error occured, <b>Error:</b> <code>{e}</code>"
        )

    return

@app.on_callback_query(filters.regex("admin_"))
async def promote_button(_, query:CallbackQuery):
    chat = query.message.chat

    mode = query.data.split("_")[1]
    uid = query.data.split("_")[3]
    try:
        if query.from_user.id != int(uid):
            return await query.answer("NOT YOUR BUTTON!")
        if mode == "demote":
            user_id = query.data.split("_")[2]
            user_member = await chat.get_member(user_id)
            await query.message.chat.promote_member(
                    user_id=user_id,
                    privileges=ChatPrivileges(
                         can_change_info=False,
                         can_invite_users=False,
                         can_delete_messages=False,
                         can_restrict_members=False,
                         can_pin_messages=False,
                         can_promote_members=False,
                         can_manage_chat=False,
                         can_manage_video_chats=False,
                ))
            await query.message.delete()
            await app.answer_callback_query(
                    query.id,
                    f"Sucessfully demoted {user_member.user.first_name or user_id}",
                    show_alert=True,
                )
                
        elif mode == "lpromote":
            user_id = query.data.split("_")[2]
            user_member = await chat.get_member(user_id)
            await query.message.chat.promote_member(
                    user_id=user_id,
                    privileges=ChatPrivileges(
                         can_change_info=False,
                         can_invite_users=True,
                         can_delete_messages=True,
                         can_restrict_members=False,
                         can_pin_messages=False,
                         can_promote_members=False,
                         can_manage_chat=False,
                         can_manage_video_chats=True,
                ))
            await query.message.delete()
            await app.answer_callback_query(
                    query.id,
                    f"Sucessfully Low Promoted {user_member.user.first_name or user_id}",
                    show_alert=True,
                )
        elif mode == "delete":
            await query.message.delete()
            await app.answer_callback_query(
                    query.id,
                    f"CANCELLED THE PROCESS",
                    show_alert=True,
                )
        elif mode == "fpromote":
            user_id = query.data.split("_")[2]
            user_member = await chat.get_member(user_id)
            await query.message.chat.promote_member(
                    user_id=user_id,
                    privileges=ChatPrivileges(
                         can_change_info=True,
                         can_invite_users=True,
                         can_delete_messages=True,
                         can_restrict_members=True,
                         can_pin_messages=True,
                         can_promote_members=False,
                         can_manage_chat=True,
                         can_manage_video_chats=True,
                ))
            await query.message.delete()
            await app.answer_callback_query(
                    query.id,
                    f"Sucessfully Full Promoted {user_member.user.first_name or user_id}",
                    show_alert=True,
                )
    except BadRequest as excp:
        pass


@app.on_message(filters.command("demote", COMMAND_HANDLER))
@bot_admin
@bot_can_promote
@user_admin
@user_can_promote
async def demote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text("I can't demote nothing.")
        return
    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return
    if user_id == BOT_ID:
        await m.reply_text("Get an admin to demote me!")
        return
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "demote_cache_update"))
        }
    if user_id not in admin_list:
        await m.reply_text(
            "This user is not an admin, how am I supposed to re-demote them?",
        )
        return
    keyboard= InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data=f"admin_demote_{user_id}_{m.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text="❌",
                        callback_data=f"admin_delete_{user_id}_{m.from_user.id}",
                    ),
                ],
            ],
        )
    await m.reply_text(f"""
<b>• EVENT: DEMOTE
➖➖➖➖➖➖➖➖➖➖➖➖
- ADMIN: {await mention_html(m.from_user.first_name, m.from_user.id)}
- USER: {await mention_html(user_first_name, user_id)}
➖➖➖➖➖➖➖➖➖➖➖➖</b>
""",
        reply_markup=keyboard,
    )
    return


@app.on_message(filters.command("invitelink", COMMAND_HANDLER))
@user_admin
@bot_admin
async def get_invitelink(c: app, m: Message):
    if m.from_user.id not in OWNER:
        user = await m.chat.get_member(m.from_user.id)
        if not user.privileges.can_invite_users and user.status != CMS.OWNER:
            await m.reply_text(text="You don't have rights to invite users....")
            return False
    try:
        link = await c.export_chat_invite_link(m.chat.id)
        await m.reply_text(
            text=f"Invite Link for Chat <b>{m.chat.id}</b>:",
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("LINK", url=f"{link}")
                ]
            ]
            ),
            disable_web_page_preview=True,
        )
    except ChatAdminInviteRequired:
        await m.reply_text(text="I don't have permission for invite link!")
    except RPCError as ef:
        await m.reply_text(
            text=f"Some error occured,\n <b>Error:</b> <code>{ef}</code>"
        )
    return


@app.on_message(filters.command("setgtitle", COMMAND_HANDLER))
@user_admin
@user_can_change_info
@bot_admin
@bot_can_change_info
async def setgtitle(_, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_change_info and user.status != CMS.OWNER:
        await m.reply_text(
            "You don't have enough permission to use this command!",
        )
        return False
    if len(m.command) < 1:
        return await m.reply_text("Please read /help for using it!")
    gtit = m.text.split(None, 1)[1]
    try:
        await m.chat.set_title(gtit)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"Successfully Changed Group Title From {m.chat.title} To {gtit}",
    )

@app.on_message(filters.command("setgdesc", COMMAND_HANDLER))
@user_admin
@user_can_change_info
@bot_admin
@bot_can_change_info
async def setgdes(_, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_change_info and user.status != CMS.OWNER:
        await m.reply_text(
            "You don't have enough permission to use this command!",
        )
        return False
    if len(m.command) < 1:
        return await m.reply_text("Please read /help for using it!")
    desp = m.text.split(None, 1)[1]
    try:
        await m.chat.set_description(desp)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"Successfully Changed Group description From {m.chat.description} To {desp}",
    )


@app.on_message(filters.command("title", COMMAND_HANDLER))
@user_admin
@user_can_promote
@bot_admin
@bot_can_promote
async def set_user_title(c: app, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_promote_members and user.status != CMS.OWNER:
        await m.reply_text(
            "You don't have enough permission to use this command!",
        )
        return False
    if len(m.text.split()) == 1 and not m.reply_to_message:
        return await m.reply_text("To whom??")
    if m.reply_to_message:
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return
    if not user_id:
        return await m.reply_text("Cannot find user!")
    if user_id == BOT_ID:
        return await m.reply_text("Huh, why ?")
    if not reason:
        return await m.reply_text("Read /help please!")
    from_user = await c.get_users(user_id)
    title = reason
    try:
        await c.set_administrator_title(m.chat.id, from_user.id, title)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"Successfully Changed {from_user.mention}'s Admin Title To {title}",
    )

@app.on_message(filters.command("setgpic", COMMAND_HANDLER))
@user_admin
@user_can_change_info
@bot_admin
@bot_can_change_info
async def set_chat_photo(_, ctx: Message):
    reply = ctx.reply_to_message
    if not reply:
        return await ctx.reply_text("Reply to a photo to set it as chat_photo")
    file = reply.document or reply.photo
    if not file:
        return await ctx.reply_text(
            "Reply to a photo or document to set it as chat photo"
        )
    if file.file_size > 5000000:
        return await ctx.reply("File size too large.")
    photo = await reply.download()
    try:
        await ctx.chat.set_photo(photo=photo)
        await ctx.reply_text("Successfully Changed Group Photo")
    except Exception as err:
        await ctx.reply(f"Failed changed group photo. ERROR: {err}")
    os.remove(photo)