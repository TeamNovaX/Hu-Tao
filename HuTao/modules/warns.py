import asyncio
from pyrogram import filters

from HuTao import app, BOT_ID, OWNER, COMMAND_HANDLER, BOT_USERNAME
from HuTao.helpers.status import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from pyrogram.enums import ChatMemberStatus

from HuTao.helpers.extraction import extract_user
from HuTao.database.warns_db import *
from HuTao.helpers.parser import mention_html
from HuTao.helpers.cache import ADMIN_CACHE, admin_cache_reload



@app.on_message(filters.command(["warn","dwarn"], COMMAND_HANDLER))
@bot_admin
@bot_can_ban
@user_admin
async def warns(app, message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("Give A ID or Reply To A User To Mute!")
        return

    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    
    chat_id = message.chat.id
    reason = None
    if message.reply_to_message:
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
    else:
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]

    if not user_id:
        await message.reply_text("That looks like an invalid User ID to me.")
        return 
    if user_id == BOT_ID:
        await message.reply_text("Huh?")
        return 
    if user_id in OWNER:
        await message.reply_text("This user is my Owner, go cry somewhere else")
        return
    
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "warn")

    if user_id in admins_group:
        await message.reply_text(text="This user is an admin, I cannot Warn them!")
        return
    
    user, warns = await asyncio.gather(app.get_users(user_id),get_warn(chat_id, await int_to_alpha(user_id)),) 

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    if warns:
        warns = warns["warns"]
    else:
        warns = 0
    
    dmsg = f"""
**ACTION: D - WARN
➖➖➖➖➖➖➖➖➖➖➖➖➖
» USER:{mention}
» BY: {message.from_user.mention if message.from_user else 'Anon'}
» COUNT: {warns + 1}/3

» REASON: {reason or 'None'}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🔹 READ THE RULES TO AVOID GETTING MORE WARNS!**
"""
    
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
        return await message.reply_text(dmsg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("REMOVE WARN",callback_data=f"unwarn_{user_id}")],[InlineKeyboardButton("RULES", url=f"https://t.me/{BOT_USERNAME}?start=rules_{chat_id}")]]))
    
    if warns >= 2:
        await app.ban_chat_member(chat_id,user_id)
        await message.reply_text(f"""
**ACTION: WARN-BAN
➖➖➖➖➖➖➖➖➖➖➖➖➖
» USER: {mention} 

» REASON: Warn Limit Exceded 
➖➖➖➖➖➖➖➖➖➖➖➖➖**""")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}

        msg = f"""
**ACTION: WARN
➖➖➖➖➖➖➖➖➖➖➖➖➖
» USER: {mention}
» BY: {message.from_user.mention if message.from_user else 'Anon'}
» COUNT: {warns + 1}/3

» REASON: {reason or 'None'}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🔹 READ THE RULES TO AVOID GETTING MORE WARNS!**
"""
        await message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("REMOVE WARN",callback_data=f"unwarn_{user_id}")],[InlineKeyboardButton("RULES", url=f"https://t.me/{BOT_USERNAME}?start=rules_{chat_id}")]]))
        await add_warn(chat_id, await int_to_alpha(user_id), warn)
 

@app.on_callback_query(filters.regex(r"unwarn_(.*)"))
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    user = await cq.message.chat.get_member(cq.from_user.id)
    
    if not user.status != ChatMemberStatus.ADMINISTRATOR or user.status != ChatMemberStatus.OWNER:
        return await cq.answer("YOU DONT HAVE ENOUGH PERMISSONS DO IT", show_alert=True,)

    user_id = cq.data.split("_")[1]

    warns = await get_warn(chat_id, await int_to_alpha(user_id))

    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("User has no warnings.", show_alert=True)

    warn = {"warns": warns - 1}

    await add_warn(chat_id, await int_to_alpha(user_id), warn)

    text = f"**WARN REMOVED BY: {from_user.mention}\n\nCOUNT: {warns}**"

    await cq.message.edit(text)


@app.on_message(filters.command(["rmwarns","resetwarns"], COMMAND_HANDLER))
@user_admin
@bot_admin
async def remove_warnings(_, message: Message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("Give A ID or Reply To A User To Mute!")
        return

    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    
    chat_id = message.chat.id

    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    mention = await mention_html("USER", user_id)

    if warns:
        warns = warns["warns"]

    if warns == 0 or not warns:
        await message.reply_text(f"{mention} **HAVE NO WARNINGS IN THIS CHAT**")

    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"**REMOVED THE WARNINGS OF: {mention}**.\n\n**CURRENT WARNS: {warns - 1}**")