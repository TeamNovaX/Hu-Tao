from pyrogram import filters 
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery ,ChatPermissions
from pyrogram.errors import BadRequest 

from HuTao.database.approve_db import approved_users
from HuTao.database.fsub_db import *
from HuTao.helpers.status import user_admin, bot_admin, bot_can_ban

from HuTao import app, BOT_ID, COMMAND_HANDLER, OWNER

@app.on_message(filters.command("fsub", COMMAND_HANDLER) & filters.group)
@user_admin
@bot_admin
@bot_can_ban
async def force_sub(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split()
    user = await _.get_chat_member(chat_id,user_id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("You Need To Be Owner Of This Chat To Enable Force Sub")           
    if "OFF".lower() in args:
         await fsub_off(chat_id)
         return await message.reply_text("**Disabled Force-Sub in This Chat**")
    elif len(args) < 2:
        return await message.reply_text("Give Me A Channel ID or Username To Enable Force-Sub")
    ch = args[1]
    try:
        channel = await _.get_chat(ch)
    except:
        return await message.reply_text("Not A Valid Channel Username")
    try:
        await _.get_chat_member(channel.id,BOT_ID)
    except BadRequest :
        return await message.reply_text("Make Sure That I Am Admin In The Channel")
    member = await _.get_chat_member(channel.id,BOT_ID)
    if member.status != ChatMemberStatus.ADMINISTRATOR:
        return await message.reply_text("I Am Not Admin In The Channel. Add Me In The Channel As An Admin First", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("CHANNEL", url=f"https://t.me/{ch}")]]))

    await fsub_on(chat_id,channel.id)
    await message.reply_text(f"Successfully Enabled Force-Sub For @{channel.username}.")

@app.on_message(filters.command("fsub_stats") & filters.group)
@user_admin
async def force_stat(_, message):
    chat_id = message.chat.id
    status = await fsub_stat(chat_id)
    if status is True:
        channel = await _.get_chat(await get_channel(chat_id)) 
        return await message.reply_text(f"Force-Sub is Enabled For [This Channel](t.me/{channel.username})")
    return await message.reply_text("Force-Sub is Disabled For This Chat")

@app.on_message(group=4)
async def fsmute(_, message):
    chat_id = message.chat.id
    if not await fsub_stat(chat_id):
        return
    if not message.from_user:
        return
    SUPREME = await approved_users(chat_id) + OWNER    
    async for m in _.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        SUPREME.append(m.user.id)

    if message.from_user.id in SUPREME:
        return 
    
    ch = await get_channel(chat_id)
    channel = await _.get_chat(ch)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("JOIN CHANNEL",url=f"t.me/{channel.username}"), InlineKeyboardButton("UNMUTE ME", callback_data=f"fsubuser_{message.from_user.id}")]])
    msg = f"{message.from_user.mention}, YOU HAVE NOT SUBSCRIBED TO [CHANNEL](t.me/{channel.username}) YET! MAKE SURE TO JOIN THE CHANNEL AND CLICK ON UNMUTE ME!"
    await message.reply_text(msg, reply_markup=buttons)
    try:
        await _.restrict_chat_member(chat_id, message.from_user.id, ChatPermissions(can_send_messages=False))
    except Exception as e:
        await message.reply_text(e)
  
@app.on_callback_query(filters.regex(pattern=r"fsubuser_(.*)"))
async def ok(_:app, query : CallbackQuery):
    muted_user = int(query.data.split("_")[1])
    chat_id = query.message.chat.id
    ch = await get_channel(chat_id)
    members = []
    async for member in _.get_chat_members(ch):
        members.append(member.user.id)
    user_id = query.from_user.id
    if user_id != muted_user:
        await query.answer(query.id,text="Not For You", show_alert=True)
        return   
              
    if not muted_user in members:
        return await query.answer(query.id,text="You Havent Joined The Channel Yet", show_alert=True)
    
    try :
        await _.unban_chat_member(chat_id, muted_user)
    except Exception as er:
        print(er)
    await query.message.delete()
