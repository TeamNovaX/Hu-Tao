import asyncio
import random
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message
)
from pyrogram.errors import WebpageCurlFailed, WebpageMediaEmpty
from HuTao import (
    BOT_NAME,
    app
)
from HuTao.Config import COMMAND_HANDLER
from HuTao.utils.data_parser import get_anime 

from HuTao.utils.helper import (
    clog,
    get_btns,
    control_user,
    get_user_from_channel as gcc,
    AUTH_USERS
)
from HuTao.utils.db import get_collection

GROUPS = get_collection("GROUPS")
SFW_GRPS = get_collection("SFW_GROUPS")
DC = get_collection('DISABLED_CMDS')
AG = get_collection('AIRING_GROUPS')
CG = get_collection('CRUNCHY_GROUPS')
SG = get_collection('SUBSPLEASE_GROUPS')
HD = get_collection('HEADLINES_GROUPS')
MHD = get_collection('MAL_HEADLINES_GROUPS')

CHAT_OWNER = ChatMemberStatus.OWNER
MEMBER = ChatMemberStatus.MEMBER
ADMINISTRATOR = ChatMemberStatus.ADMINISTRATOR

failed_pic = "https://telegra.ph/file/09733b49f3a9d5b147d21.png"
no_pic = [
    'https://telegra.ph/file/0d2097f442e816ba3f946.jpg',
    'https://telegra.ph/file/5a152016056308ef63226.jpg',
    'https://telegra.ph/file/d2bf913b18688c59828e9.jpg',
    'https://telegra.ph/file/d53083ea69e84e3b54735.jpg',
    'https://telegra.ph/file/b5eb1e3606b7d2f1b491f.jpg'
]

@app.on_message(filters.command(["anime"], COMMAND_HANDLER))
@control_user
async def anime_cmd(client: Client, message: Message, mdata: dict):
    """Search Anime Info"""
    text = mdata['text'].split(" ", 1)
    gid = mdata['chat']['id']
    try:
        user = mdata['from_user']['id']
        auser = mdata['from_user']['id']
    except KeyError:
        user = mdata['sender_chat']['id']
        ufc = await gcc(user)
        if ufc is not None:
            auser = ufc
        else:
            auser = user
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'anime' in find_gc['cmd_list'].split():
        return
    if len(text) == 1:
        k = await message.reply_text(
"""Please give a query to search about
example: /anime Ao Haru Ride"""
        )
        await asyncio.sleep(5)
        return await k.delete()
    query = text[1]
    auth = False
    vars_ = {"search": query}
    if query.isdigit():
        vars_ = {"id": int(query)}
    if (await AUTH_USERS.find_one({"id": auser})):
        auth = True
    result = await get_anime(
        vars_,
        user=auser,
        auth=auth,
        cid=gid if gid != user else None
    )
    if len(result) != 1:
        title_img, finals_ = result[0], result[1]
    else:
        k = await message.reply_text(result[0])
        await asyncio.sleep(5)
        return await k.delete()
    buttons = get_btns("ANIME", result=result, user=user, auth=auth)
    if await (
        SFW_GRPS.find_one({"id": gid})
    ) and result[2].pop() == "True":
        await client.send_photo(
            gid,
            no_pic[random.randint(0, 4)],
            caption="This anime is marked 18+ and not allowed in this group"
        )
        return
    try:
        await client.send_photo(
            gid, title_img, caption=finals_, reply_markup=buttons
        )
    except (WebpageMediaEmpty, WebpageCurlFailed):
        await clog('ANIBOT', title_img, 'LINK', msg=message)
        await client.send_photo(
            gid, failed_pic, caption=finals_, reply_markup=buttons
        )