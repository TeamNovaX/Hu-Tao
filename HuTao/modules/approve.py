from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant

from HuTao import app, OWNER, COMMAND_HANDLER
from HuTao.helpers.status import user_admin, bot_admin
from HuTao.helpers.extraction import extract_user
from HuTao.database.approve_db import *
from HuTao.helpers.parser import mention_html

@app.on_message(filters.command("approve", COMMAND_HANDLER)& filters.group)
@user_admin
@bot_admin
async def approve(_, message):
    chat_id = message.chat.id

    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    
    if not user_id:
        await message.reply_text("**I don't know who you're talking about, you're going to need to specify a user!**")
    
    try:
        member = await message.chat.get_member(user_id)
    except UserNotParticipant:
        await message.reply_text("This user is not in this chat!")
        return  

    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await message.reply_text("User is already admin - blacklists and locks already don't apply to them.",)
        return
    
    check_user = await isApproved(chat_id, user_id)
    user = await mention_html("User", user_id)

    if check_user:
        return await message.reply_photo("https://graph.org//file/49f86e096c434f3a2dc0d.jpg", caption=f"**Isn't {user} Already Approved?**")
    
    await approve_user(chat_id, user_id)
    return await message.reply_photo("https://graph.org//file/455a0e00eeaa55dce59f1.jpg", caption=f"""
**ACTION: APPROVAL
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {user}
BY: {message.from_user.mention}
➖➖➖➖➖➖➖➖➖➖➖➖➖**

**NOTE: They will now be ignored by blacklists, locks and antiflood!**""")


@app.on_message(filters.command(["disapprove", "unapprove"], COMMAND_HANDLER)& filters.group)
@user_admin
@bot_admin
async def disapprove(_, message):
    chat_id = message.chat.id

    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    
    if not user_id:
        await message.reply_text("**I don't know who you're talking about, you're going to need to specify a user!**")
    
    try:
        member = await message.chat.get_member(user_id)
    except UserNotParticipant:
        await message.reply_text("This user is not in this chat!")
        return  

    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await message.reply_text("User is admin, Cannot Disapprove Them",)
        return
 
    check_user = await isApproved(chat_id, user_id)
    user = await mention_html("User", user_id)

    if not check_user:
        return await message.reply_photo("https://graph.org//file/49f86e096c434f3a2dc0d.jpg", caption=f"**{user} Isn't Approved In This Chat**")
    
    await disapprove_user(chat_id, user_id)
    return await message.reply_photo("https://graph.org//file/455a0e00eeaa55dce59f1.jpg", caption=f"""
**ACTION: DISAPPROVAL
➖➖➖➖➖➖➖➖➖➖➖➖➖
USER: {user}
BY: {message.from_user.mention}
➖➖➖➖➖➖➖➖➖➖➖➖➖**""")


@app.on_message(filters.command("approved", COMMAND_HANDLER)& filters.group)
@user_admin
async def approvedlist(_, message):
    chat_id = message.chat.id
    list1 = await approved_users(chat_id)
    if not list:
        return await message.reply_text("**No Approved User Found**")
    text = "List Of Approved Users In This Chat:\n"
    for i in list1:
        try:
            member = await _.get_chat_member(chat_id,int(i))
            text += f"- {member.user.id}: {member.user.mention}\n"
        except:
            pass
    await message.reply_text(text)   


@app.on_message(filters.command("disapproveall", COMMAND_HANDLER) & filters.group)                 
async def disappall(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    m = await _.get_chat_member(chat_id,user_id)
    if m.status != ChatMemberStatus.OWNER:
        return await message.reply_text("**Only Owner Of This Chat Can Disapprove All Users In The Chat*")
    list1 = await approved_users(chat_id)
    if list1 is None:
        return await message.reply_text("**No Approved Users Found In This Chat**")
    
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("UNAPPROVE ALL", callback_data="unaproveall")]])

    await message.reply_photo("https://graph.org//file/ea127c118c4d47a6ceb80.jpg", caption="**Are You Sure? To Unapprove All The Users In This Chat?**",reply_markup=btn)

@app.on_callback_query(filters.regex("unaproveall"))             
async def unappall(_, query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    m = await _.get_chat_member(chat_id,user_id)
    if m.status != ChatMemberStatus.OWNER or user_id not in OWNER:
        return await query.answer("Only Owner Of This Group Can Unapprove All",show_alert=True)
    list1 = await approved_users(chat_id)
    await query.message.edit_text("``Disapproving All The Users...``")

    for user in list1:
        await disapprove_user(chat_id,int(user))
    return await query.message.edit_text("**Successfully Disapproved All The Users In This Chat**")
     
        

__mod__ = "APPROVALS"
__help__ = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.
That's what approvals are for - approve of trustworthy users to allow them to send

**» Admin commands:**
» /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
» /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
» /approved: List all approved users.
» /disapproveall: Unapprove ALL users in a chat. This cannot be undone.
"""
