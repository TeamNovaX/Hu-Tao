
from pyrogram import filters
from pyrogram.types import Message

from HuTao.database.imposter_db import (
    add_userdata,
    usr_data,
    get_userdata,
    check_imposter,
    impo_on,
    impo_off,
)
from HuTao import app
from HuTao.Config import COMMAND_HANDLER
from HuTao.helpers.status import user_admin

@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=1)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_imposter(message.chat.id):
        return
    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
🔹 IMPOSTER DETECTED 👀:
➖➖➖➖➖➖➖➖➖➖➖➖
▪️User: {message.from_user.mention}
▪️ID: {message.from_user.id}
➖➖➖➖➖➖➖➖➖➖➖➖\n
"""
    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "NO USERNAME"
        usernameafter = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "NO USERNAME"
        )
        msg += """
🔹CHANGED USERNAME:
➖➖➖➖➖➖➖➖➖➖➖➖
▪️FROM: {bef}
▪️TO: {aft}
➖➖➖➖➖➖➖➖➖➖➖➖\n
""".format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += """
🔹CHANGED FIRST NAME:
➖➖➖➖➖➖➖➖➖➖➖➖
▪️FROM: {bef}
▪️TO: {aft}
➖➖➖➖➖➖➖➖➖➖➖➖\n
""".format(
            bef=first_name, aft=message.from_user.first_name
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "NO LAST NAME"
        lastname_after = message.from_user.last_name or "NO LAST NAME"
        msg += """
🔹CHANGED LAST NAME:
➖➖➖➖➖➖➖➖➖➖➖➖
▪️FROM: {bef}
▪️TO: {aft}
➖➖➖➖➖➖➖➖➖➖➖➖\n
""".format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        await message.reply_photo("https://graph.org//file/a5f944533dcaccfaf2567.jpg", caption=msg)


@app.on_message(filters.group & filters.command("imposter", COMMAND_HANDLER) & ~filters.bot & ~filters.via_bot)
@user_admin
async def set_mataa(_, message: Message):
    if len(message.command) == 1:
        return await message.reply("Check help Section For Getting Help")
    if message.command[1] == "on":
        cekset = await impo_on(message.chat.id)
        if cekset:
            await message.reply("Imposter Mode Is Already Enabled")
        else:
            await impo_on(message.chat.id)
            await message.reply(f"Successfully Enabled Imposter Mode For {message.chat.title}")
    elif message.command[1] == "off":
        cekset = await impo_off(message.chat.id)
        if not cekset:
            await message.reply("Imposter Mode Is Already Disabled")
        else:
            await impo_off(message.chat.id)
            await message.reply(f"Successfully Enabled Imposter Mode For {message.chat.title}")
    else:
        await message.reply("Check help Section For Getting Help")



__mod__ = "IMPOSTER"
__help__ = """
**» /imposter on/off** - Turn On The Watcher For Your Group Which Notifies About User Who Change Name or Username
"""