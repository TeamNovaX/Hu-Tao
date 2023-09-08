#MIT License
#Copyright (c) 2023, ©NovaNetworks

import re

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from HuTao import BOT_NAME, BOT_USERNAME, HELPABLE, app, Hutao_Ver
from HuTao.helpers import paginate_modules
from HuTao.Config import COMMAND_HANDLER
import HuTao.sql.rules_sql as sql
from HuTao.helpers.string import *
from HuTao.modules.notes import note_redirect


PM_TEXT = f"""
**────「 {BOT_NAME} 」────
➖➖➖➖➖➖➖➖➖➖➖➖➖
¤ I'M HERE! IF YOU NEED SOME ASSISTANCE, I'M HERE TO GIVE IT MY ALL TO THE VERY END!
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
♦ VERSION: {Hutao_Ver}
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⍟ GET TO KNOW ABOUT MY SKILLS BY CLICKING HELP**
➖➖➖➖➖➖➖➖➖➖➖➖➖
"""


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="ADD ME",url=f"http://t.me/{BOT_USERNAME}?startgroup=new")
        ],
        [
            InlineKeyboardButton(text="DEVELOPER", url="https://t.me/KIRITO1240"),
            InlineKeyboardButton(text="SOURCE",url="https://t.me/NovaNetworks"),
        ],
        [
            InlineKeyboardButton(text="HELP", callback_data="help_commands")           
        ],
    ]
)


keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="HELP", url=f"t.me/{BOT_USERNAME}?start=help")
        ]
    ]
)


@app.on_message(filters.command("start", COMMAND_HANDLER))
async def start(_, message: Message):
    if message.chat.type.value != "private":
        return await message.reply_photo(
            photo="https://graph.org//file/de94bb9e07ec7bd86123d.jpg",
            caption="With every step I take, I leave a trail of ashes and memories.",
            reply_markup=keyboard,
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if "help_" in name:
            module = name.split("help_", 1)[1]
            text = (
                "**⍟ HELP FOR: {mod}**\n".format(mod=HELPABLE[module].__mod__)
                + HELPABLE[module].__help__
            )
            await message.reply_photo("https://graph.org//file/9e756c52fdd881b44ecc8.png",caption=text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("BACK", callback_data="help_back")]]
            ))
        if name == "help":
            text, keyb = await help_parser(BOT_NAME)
            await message.reply_photo(
                "https://graph.org//file/9e756c52fdd881b44ecc8.png",
                caption=text,
                reply_markup=keyb,
            )
        if "rules_" in name:
            cid = name.split("rules_", 1)[1]
            rules = sql.get_rules(cid)
            textt = rules
            await message.reply(f"**RULES FOR THIS CHAT ARE:**\n\n{textt}")
        
        if "note_" in name:
            await note_redirect(message)
    else:
        await message.reply_photo(
            photo="https://graph.org//file/2bba048fefef637247d6a.png",
            caption=PM_TEXT,
            reply_markup=home_keyboard_pm,
        )

@app.on_message(filters.command("help", COMMAND_HANDLER))
async def help_command(_, message: Message):
    if message.chat.type.value != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{name}",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply_text(
                    "**CLICK HERE TO GET HELP ABOUT: {btn_name}**".format(btn_name=name),
                    reply_markup=key,
                )
            else:
                await message.reply_text("**LETS HEAD TO PRIVATE CHAT TO KNOW MORE ABOUT MY SKILLS**", reply_markup=keyboard)
        else:
            await message.reply_text("**LETS HEAD TO PRIVATE CHAT TO KNOW MORE ABOUT MY SKILLS**", reply_markup=keyboard)
    elif len(message.command) >= 2:
        name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
        if str(name) in HELPABLE:
            text = (
                "**⍟ HELP FOR: {mod}**\n".format(mod=HELPABLE[name].__mod__)
                + HELPABLE[name].__help__
            )
            await message.reply_photo("https://graph.org//file/9e756c52fdd881b44ecc8.png",caption=text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("BACK", callback_data="help_back")]]
            ))
        else:
            text, help_keyboard = await help_parser(message.from_user.first_name)
            await message.reply_photo(
                "https://graph.org//file/9e756c52fdd881b44ecc8.png",
                caption=text,
                reply_markup=help_keyboard
            )
    else:
        text, help_keyboard = await help_parser(message.from_user.first_name)
        await message.reply_photo(
            "https://graph.org//file/9e756c52fdd881b44ecc8.png",
            caption=text, reply_markup=help_keyboard
        )



async def help_parser(name, hkey=None):
    if not hkey:
        hkey = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
"""
**────「 {BOT_NAME} 」────
➖➖➖➖➖➖➖➖➖➖➖➖➖
¤ I'm here! If you need some assistance, I'm here to give it my all to the very end!
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⍟ CLICK BELOW TO KNOW ABOUT MY SKILLS**
➖➖➖➖➖➖➖➖➖➖➖➖➖

""".format(
            BOT_NAME=BOT_NAME
        ),
        hkey,
    )

@app.on_callback_query(filters.regex("help_commands"))
async def commands_callbacc(_, cb: CallbackQuery):
    text, keyb = await help_parser(BOT_NAME)
    await cb.edit_message_caption(
        caption=text,
        reply_markup=keyb,
    )

@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(self: Client, query: CallbackQuery):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    if mod_match:
        module = mod_match[1].replace(" ", "_")
        text = (
            "**⍟ HELP FOR: {mod}**\n".format(mod=HELPABLE[module].__mod__)
            + HELPABLE[module].__help__
        )

        await query.edit_message_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("BACK", callback_data="help_back")]]
            )
        )
    elif home_match:
        await query.edit_message_caption(
            caption=PM_TEXT,
            reply_markup=home_keyboard_pm,
        )
    elif prev_match:
        curr_page = int(prev_match[1])
        await query.edit_message_caption(
            caption=f"""
**────「 {BOT_NAME} 」────
➖➖➖➖➖➖➖➖➖➖➖➖➖
¤ I'm here! If you need some assistance, I'm here to give it my all to the very end!
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⍟ CLICK BELOW TO KNOW ABOUT MY SKILLS**
➖➖➖➖➖➖➖➖➖➖➖➖➖

""",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            )
        )

    elif next_match:
        next_page = int(next_match[1])
        await query.edit_message_caption(
            caption=f"""
**────「 {BOT_NAME} 」────
➖➖➖➖➖➖➖➖➖➖➖➖➖
¤ I'm here! If you need some assistance, I'm here to give it my all to the very end!
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⍟ CLICK BELOW TO KNOW ABOUT MY SKILLS**
➖➖➖➖➖➖➖➖➖➖➖➖➖

""",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            )
        )

    elif back_match:
        await query.edit_message_caption(
            caption=f"""
**────「 {BOT_NAME} 」────
➖➖➖➖➖➖➖➖➖➖➖➖➖
¤ I'm here! If you need some assistance, I'm here to give it my all to the very end!
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⍟ CLICK BELOW TO KNOW ABOUT MY SKILLS**
➖➖➖➖➖➖➖➖➖➖➖➖➖

""",
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
        )

    elif create_match:
        text, keyb = await help_parser(query)
        await query.edit_message_caption(
            caption=text,
            reply_markup=keyb
        )

    try:
        await self.answer_callback_query(query.id)
    except:
        pass
