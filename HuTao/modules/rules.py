from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from HuTao import app, BOT_USERNAME
import HuTao.sql.rules_sql as sql
from HuTao.helpers.kbhelpers import ikb
from HuTao.helpers.string import build_keyboard, parse_button
from HuTao.Config import COMMAND_HANDLER
from HuTao.helpers import *



@app.on_message(filters.command("rules", COMMAND_HANDLER) & filters.group)
@user_admin
async def get_rules(_, m: Message):
    msg_id = m.reply_to_message.id if m.reply_to_message else m.id

    rules = sql.get_rules(m.chat.id)
    if m and not m.from_user:
        return

    if not rules:
        await m.reply_text(
            text="The group admins haven't set any rules for this chat yet. This probably doesn't mean it's lawless though...!",
            quote=True,
        )
        return

    priv_rules_status = sql.get_private_rules(m.chat.id)

    if priv_rules_status:
        pm_kb = ikb(
            [
                [
                    (
                        "Rules",
                        f"https://t.me/{BOT_USERNAME}?start=rules_{m.chat.id}",
                        "url",
                    ),
                ],
            ],
        )
        await m.reply_text(
            text="Click on the below button to see this group rules!",
            quote=True,
            reply_markup=pm_kb,
            reply_to_message_id=msg_id,
        )
        return

    formated = rules
    teks, button = await parse_button(formated)
    button = await build_keyboard(button)
    button = ikb(button) if button else None
    textt = teks
    await m.reply_text(
        text=f"""The rules for <b>{m.chat.title} are:</b>
{textt}""",
        disable_web_page_preview=True,
        reply_to_message_id=msg_id,
        reply_markup=button
    )
    return


@app.on_message(filters.command("pmrules", COMMAND_HANDLER) & filters.group)
@user_admin
async def priv_rules(_, m: Message):
    if m and not m.from_user:
        return

    if len(m.text.split()) == 2:
        option = (m.text.split())[1]
        if option in ("on", "yes"):
            sql.private_rules(str(m.chat.id), True)
            msg = f"Private Rules have been turned <b>on</b> for chat <b>{m.chat.title}</b>"
        elif option in ("off", "no"):
            sql.private_rules(str(m.chat.id), False)
            msg = f"Private Rules have been turned <b>off</b> for chat <b>{m.chat.title}</b>"
        else:
            msg = "Option not valid, choose from <code>on</code>, <code>yes</code>, <code>off</code>, <code>no</code>"
        await m.reply_text(msg)
    elif len(m.text.split()) == 1:
        curr_pref = sql.get_private_rules(m.chat.id)
        msg = ("Current Preference for Private rules in this chat is: <b>{}</b>").format("Enabled" if curr_pref else "Disabled")
        await m.reply_text(msg)
    else:
        await m.reply_text(text="Please check help on how to use this this command.")

    return


@app.on_message(filters.command("setrules", COMMAND_HANDLER) & filters.group)
@user_admin
async def set_rules(_, m: Message):
    if m and not m.from_user:
        return

    if m.reply_to_message and m.reply_to_message.text:
        rules = m.reply_to_message.text.markdown
    elif (not m.reply_to_message) and len(m.text.split()) >= 2:
        rules = m.text.split(None, 1)[1]
    else:
        return await m.reply_text("Provide some text to set as rules !!")

    if len(rules) > 4000:
        rules = rules[0:3949]  # Split Rules if len > 4000 chars
        await m.reply_text("Rules are shortened to 3950 characters!")

    sql.set_rules(m.chat.id, rules)
    await m.reply_text(text="Successfully set rules for this group.")
    return



@app.on_message(filters.command("clearrules", COMMAND_HANDLER) & filters.group)
@user_admin
async def clear_rules(_, m: Message):
    if m and not m.from_user:
        return

    rules = sql.get_rules(m.chat.id)
    if not rules:
        await m.reply_text(
            text="The Admins for this group have not setup rules! That doesn't mean you can break the DECORUM of this group !"
        )
        return

    await m.reply_text(
        text="Are you sure you want to clear rules?",
        reply_markup=ikb(
            [[("⚠️ Confirm", "clear_rules"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^clear_rules$"))
async def clearrules_callback(_, q: CallbackQuery):
    chat_id = q.message.chat.id
    sql.set_rules(chat_id, "")
    await q.message.edit_text(text="Successfully cleared rules for this group!")
    await q.answer("Rules for the chat have been cleared!", show_alert=True)
    return


__mod__ = "RULES"
__help__ = """
**» Set rules for you chat so that members know what to do and what not to do in your group!**

» /rules: get the rules for current chat.

**» Admin only:**
» /setrules `<rules>`: Set the rules for this chat, also works as a reply to a message.
» /clearrules: Clear the rules for this chat.
» /privrules `<on/yes/no/off>`: Turns on/off the option to send the rules to PM of user or group.
"""