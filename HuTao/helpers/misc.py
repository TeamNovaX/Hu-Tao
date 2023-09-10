#MIT License
#Copyright (c) 2023, ©NovaNetworks

from math import ceil
from pyrogram.types import InlineKeyboardButton
from HuTao import MOD_LOAD, MOD_NOLOAD

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_modules(page_n, module_dict, prefix, chat=None):
    modules = (
        sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod__,
                    callback_data=f"{prefix}_module({chat},{x.__mod__.lower()})",
                )
                for x in module_dict.values()
            ]
        )
        if chat
        else sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod__,
                    callback_data=f"{prefix}_module({x.__mod__.lower()})",
                )
                for x in module_dict.values()
            ]
        )
    )

    pairs = list(zip(modules[::3], modules[1::3], modules[2::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 3

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮", callback_data=f"{prefix}_prev({modulo_page})"
                ),
                EqInlineKeyboardButton(
                    "❯ BACK ❮", callback_data=f"{prefix}_home({modulo_page})"
                ),
                EqInlineKeyboardButton(
                    "❯", callback_data=f"{prefix}_next({modulo_page})"
                ),
            )
        ]

    return pairs

def is_module_loaded(name):
    return (not MOD_LOAD or name in MOD_LOAD) and name not in MOD_NOLOAD

async def getFile(message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        image = await message.reply_to_message.download()
        return image
    else:
        return None

async def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

ImageModels = {
    "Meina Mix":2,
    "Cetus Mix":10,
    "DarkSushiMix":9,
    "DarkSushiMix V2":14,
    "Absolute Reality":13,
    "CreativeV2":12,
}