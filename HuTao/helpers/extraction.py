from traceback import format_exc
from typing import Tuple

from pyrogram.enums import MessageEntityType as entity
from pyrogram.types.messages_and_media.message import Message

from HuTao import app
from HuTao.database.users_db import *


async def extract_user(c: app, m: Message) -> Tuple[int, str, str]:
    user_id = None
    user_first_name = None
    user_name = None

    if m.reply_to_message and m.reply_to_message.from_user:
        user_id = m.reply_to_message.from_user.id
        user_first_name = m.reply_to_message.from_user.first_name
        user_name = m.reply_to_message.from_user.username

    elif len(m.text.split()) > 1:
        if len(m.entities) > 1:
            required_entity = m.entities[1]
            if required_entity.type == entity.TEXT_MENTION:
                user_id = required_entity.user.id
                user_first_name = required_entity.user.first_name
                user_name = required_entity.user.username
            elif required_entity.type in (entity.MENTION, entity.PHONE_NUMBER):
                user_found = m.text[
                    required_entity.offset : (
                        required_entity.offset + required_entity.length
                    )
                ]

                try:
                    user_found = int(user_found)
                except (ValueError, Exception) as ef:
                    if "invalid literal for int() with base 10:" in str(ef):
                        user_found = str(user_found)
                    else:
                        pass

                try:
                    user = await get_user_info(user_found)
                    user_id = user["user_id"]
                    user_first_name = user["user_first_name"]
                    user_name = user["username"]
                except KeyError:
                    try:
                        user = await c.get_users(user_found)
                    except Exception as ef:
                        try:
                            user_r = await c.resolve_peer(user_found)
                            user = await c.get_users(user_r.user_id)
                        except Exception as ef:
                            return await m.reply_text(f"User not found ! Error: {ef}")
                    user_id = user.id
                    user_first_name = user.first_name
                    user_name = user.username
                except Exception as ef:
                    user_id = user_found
                    user_first_name = user_found
                    user_name = ""

        else:
            try:
                user_id = int(m.text.split()[1])
            except (ValueError, Exception) as ef:
                if "invalid literal for int() with base 10:" in str(ef):
                    user_id = (
                        str(m.text.split()[1])
                        if (m.text.split()[1]).startswith("@")
                        else None
                    )
                else:
                    user_id = m.text.split()[1]

            if user_id is not None:
                try:
                    user = await get_user_info(user_id)
                    user_first_name = user["user_first_name"]
                    user_name = user["username"]
                except Exception as ef:
                    try:
                        user = await c.get_users(user_id)
                    except Exception as ef:
                        try:
                            user_r = await c.resolve_peer(user_found)
                            user = await c.get_users(user_r.user_id)
                        except Exception as ef:
                            return await m.reply_text(f"User not found ! Error: {ef}")
                    user_first_name = user.first_name
                    user_name = user.username

    else:
        user_id = m.from_user.id
        user_first_name = m.from_user.first_name
        user_name = m.from_user.username

    return user_id, user_first_name, user_name