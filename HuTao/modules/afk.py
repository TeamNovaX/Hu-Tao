import time
import re
import random

from pyrogram import filters, enums, Client
from pyrogram.types import Message

from HuTao.database.afk_db import add_afk, is_afk, remove_afk
from HuTao import app
from HuTao.helpers.errors import capture_err
from HuTao.helpers.readable_time import get_readable_time2


# Handle set AFK Command
@app.on_message(filters.command(["afk"]))
async def active_afk(self: Client, ctx: Message):
    if ctx.sender_chat:
        return await ctx.reply_text("You can only use this command in a private chat.", del_in=6)

    user_id = ctx.from_user.id
    verifier, reasondb = await is_afk(user_id)

    if verifier:
        await remove_afk(user_id)

        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))

            if afktype == "animation":
                send = (
                    await ctx.reply_animation(data, caption=f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}.")
                    if str(reasonafk) == "None"
                    else await ctx.reply_animation(data, caption=f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}. Reason: {reasonafk}")
                )
            elif afktype == "photo":
                send = (
                    await ctx.reply_photo(photo=f"downloads/{user_id}.jpg", caption=f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}.")
                    if str(reasonafk) == "None"
                    else await ctx.reply_photo(photo=f"downloads/{user_id}.jpg", caption=f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}. Reason: {reasonafk}")
                )
            elif afktype == "text":
                send = await ctx.reply_text(f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}.", disable_web_page_preview=True)
            elif afktype == "text_reason":
                send = await ctx.reply_text(f"{ctx.from_user.mention} [`{ctx.from_user.id}`] is no longer AFK for {seenago}. Reason: {reasonafk}", disable_web_page_preview=True)
        except Exception:
            send = await ctx.reply_text(f"{ctx.from_user.first_name} [`{ctx.from_user.id}`] is online.", disable_web_page_preview=True)

        return

    if len(ctx.command) == 1 and not ctx.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and not ctx.reply_to_message:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "data": _data,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        _reason = ctx.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.sticker:
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(ctx.command) > 1 and ctx.reply_to_message.sticker:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    send = await ctx.reply_text(f"{ctx.from_user.mention} [`{ctx.from_user.id}`] has activated AFK mode.")
    

@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=1,
)
async def afk_watcher_func(self: Client, ctx: Message):
    if ctx.sender_chat:
        return
    userid = ctx.from_user.id
    user_name = ctx.from_user.mention
    if ctx.entities:
        possible = ["/afk", f"/afk@{self.me.username}", "!afk"]
        message_text = ctx.text or ctx.caption
        for entity in ctx.entities:
            if entity.type == enums.MessageEntityType.BOT_COMMAND:
                if (message_text[0:0 + entity.length]).lower() in possible:
                    return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "text":
                afk_messages = [
                    f"{user_name} [`{userid}`] is back. AFK for {seenago}.",
                    f"{user_name} [`{userid}`] has returned. They were AFK for {seenago}.",
                    f"{user_name} [`{userid}`] is no longer AFK.",
                    f"{user_name} [`{userid}`] is back in action! They were away for {seenago}.",
                    f"Welcome back, {user_name} [`{userid}`]! They were AFK for {seenago}.",
                ]
                msg += random.choice(afk_messages)
            if afktype == "text_reason":
                afk_messages = [
                    f"{user_name} [`{userid}`] is back. AFK for {seenago}. Reason: {reasonafk}",
                    f"{user_name} [`{userid}`] has returned. They were AFK for {seenago}. Reason: {reasonafk}",
                    f"{user_name} [`{userid}`] is no longer AFK. Reason: {reasonafk}",
                    f"{user_name} [`{userid}`] is back in action! They were away for {seenago}. Reason: {reasonafk}",
                    f"Welcome back, {user_name} [`{userid}`]! They were AFK for {seenago}. Reason: {reasonafk}",
                ]
                msg += random.choice(afk_messages)
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await ctx.reply_animation(data, caption=f"{user_name} [`{userid}`] is back. AFK for {seenago}.")
                else:
                    send = await ctx.reply_animation(data, caption=f"{user_name} [`{userid}`] is back. AFK for {seenago}. Reason: {reasonafk}")
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await ctx.reply_photo(photo=f"downloads/{userid}.jpg", caption=f"{user_name} [`{userid}`] is back. AFK for {seenago}.")
                else:
                    send = await ctx.reply_photo(photo=f"downloads/{userid}.jpg", caption=f"{user_name} [`{userid}`] is back. AFK for {seenago}. Reason: {reasonafk}")
        except:
            msg += f"{user_name} [`{userid}`] is online."

    # Replied to a User which is AFK
    if ctx.reply_to_message:
        try:
            replied_first_name = ctx.reply_to_message.from_user.mention
            replied_user_id = ctx.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time2((int(time.time() - timeafk)))
                    if afktype == "text":
                        replied_afk_messages = [
                            f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}.",
                            f"{replied_first_name} [`{replied_user_id}`] is currently away. Please expect a delayed response.",
                            f"{replied_first_name} [`{replied_user_id}`] is temporarily unavailable. They will get back to you soon.",
                            f"{replied_first_name} [`{replied_user_id}`] is AFK. Please leave a message and they will reply when they return.",
                        ]
                        msg += random.choice(replied_afk_messages)
                    if afktype == "text_reason":
                        replied_afk_messages = [
                            f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}. Reason: {reasonafk}",
                            f"{replied_first_name} [`{replied_user_id}`] is currently away. Reason: {reasonafk}",
                            f"{replied_first_name} [`{replied_user_id}`] is temporarily unavailable. Reason: {reasonafk}",
                            f"{replied_first_name} [`{replied_user_id}`] is AFK. Reason: {reasonafk} Please leave a message and they will reply when they return.",
                        ]
                        msg += random.choice(replied_afk_messages)
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_animation(data, caption=f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}.")
                        else:
                            send = await ctx.reply_animation(data, caption=f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}. Reason: {reasonafk}")
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_photo(photo=f"downloads/{replied_user_id}.jpg", caption=f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}.")
                        else:
                            send = await ctx.reply_photo(photo=f"downloads/{replied_user_id}.jpg", caption=f"{replied_first_name} [`{replied_user_id}`] is AFK for {seenago}. Reason: {reasonafk}")
                except:
                    msg += f"{replied_first_name} [`{replied_user_id}`] is online."
        except:
            pass

    # Mentioning a User which is AFK
    if ctx.entities:
        for entity in ctx.entities:
            if entity.type == enums.MessageEntityType.MENTION or entity.type == enums.MessageEntityType.TEXT_MENTION:
                try:
                    user_id_mentioned = ctx.text[entity.offset:entity.offset + entity.length].replace("@", "")
                    mentioned_user_info = await app.get_users(user_ids=int(user_id_mentioned))
                    mentioned_user_first_name = mentioned_user_info[0].mention
                    verifier, reasondb = await is_afk(int(user_id_mentioned))
                    if verifier:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time2((int(time.time() - timeafk)))
                        if afktype == "text":
                            mentioned_afk_messages = [
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}.",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is currently away. Please expect a delayed response.",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is temporarily unavailable. They will get back to you soon.",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK. Please leave a message and they will reply when they return.",
                            ]
                            msg += random.choice(mentioned_afk_messages)
                        if afktype == "text_reason":
                            mentioned_afk_messages = [
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}. Reason: {reasonafk}",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is currently away. Reason: {reasonafk}",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is temporarily unavailable. Reason: {reasonafk}",
                                f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK. Reason: {reasonafk} Please leave a message and they will reply when they return.",
                            ]
                            msg += random.choice(mentioned_afk_messages)
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_animation(data, caption=f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}.")
                            else:
                                send = await ctx.reply_animation(data, caption=f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}. Reason: {reasonafk}")
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_photo(photo=f"downloads/{user_id_mentioned}.jpg", caption=f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}.")
                            else:
                                send = await ctx.reply_photo(photo=f"downloads/{user_id_mentioned}.jpg", caption=f"{mentioned_user_first_name} [`{user_id_mentioned}`] is AFK for {seenago}. Reason: {reasonafk}")
                except:
                    pass

    if msg != "":
        await ctx.reply_text(msg)
