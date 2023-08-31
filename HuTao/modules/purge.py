from asyncio import sleep

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message

from HuTao import app, COMMAND_HANDLER
from HuTao.helpers.status import *


@app.on_message(filters.command("purge", COMMAND_HANDLER))
@bot_admin
@user_admin
@bot_can_del
@user_can_del
async def purge(c: app, m: Message):
    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text("Cannot Purge Messages Here, Upgrade Your Group To Supergroup")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text("Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup.")
            return
        except RPCError as ef:
            await m.reply_text(f"""Some error occured, Error: {ef}""")

        count_del_msg = len(message_ids)

        z = await m.reply_text(text=f"Deleted **{count_del_msg}** Messages...")
        await sleep(3)
        await z.delete()
        return
    await m.reply_text("Reply to a message to start purge !")
    return


@app.on_message(filters.command("spurge", COMMAND_HANDLER))
@bot_admin
@user_admin
@bot_can_del
@user_can_del
async def spurge(c: app, m: Message):

    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text(text="Cannot Purge Messages Here, Upgrade Your Group To Supergroup")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(
                text="Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup."
            )
            return
        except RPCError as ef:
            await m.reply_text(f"""Some error occured, Error: {ef}""")
        return
    await m.reply_text("Reply to a message to start spurge !")
    return


@app.on_message(filters.command("del", COMMAND_HANDLER))
@bot_admin
@user_admin
@bot_can_del
@user_can_del
async def del_msg(c: app, m: Message):

    if m.chat.type != ChatType.SUPERGROUP:
        return

    if m.reply_to_message:
        await m.delete()
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.reply_to_message.id,
        )
    else:
        await m.reply_text(text="What do you wanna delete?")
    return


__mod__ = "PURGE"

__help__ = """
» /purge: Deletes messages upto replied message.
» /spurge: Deletes messages upto replied message without a success message.
» /del: Deletes a single message, used as a reply to message."""
