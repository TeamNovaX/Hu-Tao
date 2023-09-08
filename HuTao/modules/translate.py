from gpytranslate import SyncTranslator
from HuTao import app, COMMAND_HANDLER
from pyrogram import filters, enums 

trans = SyncTranslator()

@app.on_message(filters.command(["tr","tl"], COMMAND_HANDLER))
async def _translate(_, message):
    text = await message.reply("Translating....")
    replied = message.reply_to_message
    if not replied:
        return await text.edit("Reply to A Message To Translate It")
    
    if replied.caption:
        to_translate = replied.caption
    elif replied.text:
        to_translate = replied.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args    
    
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"**Translated From {source} To {dest} :**\n" \
        f"`{translation.text}`"

    await text.edit(reply)       