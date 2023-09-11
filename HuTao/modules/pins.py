from HuTao import app, COMMAND_HANDLER
from pyrogram import filters 
from HuTao.helpers.status import bot_admin, user_admin, bot_can_pin

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery 
from pyrogram import Client

@app.on_message(filters.command("pin", COMMAND_HANDLER) & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def pins(_, message):
    replied = message.reply_to_message
    user_id = message.from_user.id
    if not replied:
        return await message.reply_text("Reply To A Message To Pin It!")
    try:
        await replied.pin(disable_notification=True)
        await message.reply_text("Successfully Pinned This Message",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="PINNED MESSAGE",url=replied.link)],[InlineKeyboardButton(text="UNPIN", callback_data=f"unpin_{user_id}_{replied.id}")]]))  
    except Exception as er:
        await message.reply_text(er)

@app.on_message(filters.command("pinned", COMMAND_HANDLER) & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def pinned(_, message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("No Pinned Message Found")
    try:        
        await message.reply_text("Here is The Latest Pinned Message",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="View Message",url=chat.pinned_message.link)]]))  
    except Exception as er:
        await message.reply_text(er)


@app.on_message(filters.command(["unpin"], COMMAND_HANDLER) & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def _unpinmsg(_, message):
    if message.command[0] == "unpin":
        replied = message.reply_to_message
        if not replied:
            return await message.reply_text("Reply To A Message To Unpin It!")
        try:
            await replied.unpin()
            await message.reply_text("Successfully Unpinned This Message",reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(text="MESSAGE",url=replied.link)]]))  
        except Exception as er:
            await message.reply_text(er)
    

@app.on_callback_query(filters.regex(pattern=r"unpin_(.*)"))
async def unpin_btn(app : Client, query : CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    ids = query.data.split("_")  
    if int(ids[1]) == user_id:
        await app.unpin_chat_message(chat_id,int(ids[2])) 
        await query.message.edit("**Unpinned The Message**")
    else:
        await app.answer_callback_query(
        query.id,
    text="This Message is Not Pinned By You",
    show_alert=True
)
