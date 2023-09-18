from HuTao.database import *

fsubdb = dbname["fsub"] 

async def fsub_off(chat_id):
    chat = await fsubdb.find_one({"chat_id" : chat_id})
    if chat:
        return await fsubdb.delete_one({"chat_id" : chat_id})

async def fsub_on(chat_id : int, channel: str):
    return await fsubdb.update_one({"chat_id" : chat_id},{"$set" : {"channel" : channel}}, upsert=True)

async def fsub_stat(chat_id : int) -> bool:
    chat = bool(await fsubdb.find_one({"chat_id" : chat_id}))
    return chat 

async def get_channel(chat_id : int):
    chat = await fsubdb.find_one({"chat_id" : chat_id})
    if chat:
        return chat["channel"]
    return None
