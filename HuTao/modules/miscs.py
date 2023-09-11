import os
import time
from asyncio import sleep
from blackpink import blackpink as bp

from pyrogram import enums, filters
from pyrogram.types import *

from HuTao import app, COMMAND_HANDLER


@app.on_message(filters.command("id", COMMAND_HANDLER), group=3)
async def uid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    mention_user = message.from_user.mention
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[Message ID]({message.link})** » `{message_id}`\n"
    text += f"**[{mention_user}](tg://user?id={your_id})** » `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()
        
    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            user_mention = (await client.get_users(split)).mention 
            text += f"**[{user_mention}](tg://user?id={user_id})** » `{user_id}`\n"

        except Exception:
            return await message.reply_text("**No User Found**")

    text += f"**[Chat ID](https://t.me/{chat.username})** » `{chat.id}`\n\n"

    if not getattr(reply, "empty", True) and not message.forward_from_chat and not reply.sender_chat:
        text += (
            f"**[Replied Message ID]({reply.link})** » `{message.reply_to_message.id}`\n"
        )
        text += f"**[Replied User ID](tg://user?id={reply.from_user.id})** » `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"The Forwarded Channel, {reply.forward_from_chat.title}, Has ID: `{reply.forward_from_chat.id}`\n\n"        
    
    if reply and reply.sender_chat:
        text += f"The ID of Replied Chat/Channel: `{reply.sender_chat.id}`"
        
    await message.reply(text)
      



@app.on_message(~filters.private & filters.command(["gstatus"], COMMAND_HANDLER), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("**GETTING INFORMATION...**")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for member in app.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(f"""
**➖➖➖➖➖➖➖
➲ NAME : {message.chat.title}
➲ MEMBERS : [ {count} ]
➖➖➖➖➖➖➖
➲ BOTS : {bot}
➲ ZOMBIES : {deleted_acc}
➲ BANNED : {banned}
➲ PREMIUM USERS : {premium_acc}
➖➖➖➖➖➖➖
TIME TAKEN : {timelog} S**""")
    else:
        sent_message = await message.reply_text("**ONLY ADMINS CAN USE THIS !**")
        await sleep(5)
        await sent_message.delete()


@app.on_message(filters.command("blackpink", COMMAND_HANDLER))
async def blackpink(_, message):
    text = message.text[len("/blackpink ") :]
    bp(f"{text}").save(f"blackpink_{message.from_user.id}.png")
    await message.reply_photo(f"blackpink_{message.from_user.id}.png")
    os.remove(f"blackpink_{message.from_user.id}.png")


@app.on_message(filters.video_chat_started)
async def brah(client, message):
       await message.reply("**Voice Chat Started**")

@app.on_message(filters.video_chat_ended)
async def brah2(client, message):
       await message.reply("**Voice Chat Ended**")

@app.on_message(filters.video_chat_members_invited)
async def fuckoff(client, message):
           text = f"{message.from_user.mention} Invited "
           x = 0
           for user in message.video_chat_members_invited.users:
             try:
               text += f"[{user.first_name}](tg://user?id={user.id}) "
               x += 1
             except Exception:
               pass
           try:
             await message.reply(f"{text} 😉")
           except:
             pass

