#MIT License
#Copyright (c) 2023, ©NovaNetworks

from HuTao.database import *

jreq = dbname["jrequests"] 


async def add_join(chat_id : int):
    return await jreq.insert_one({"chat_id" : chat_id})
    
async def rm_join(chat_id : int):   
    chat = await jreq.find_one({"chat_id" : chat_id})
    if chat: 
        return await jreq.delete_one({"chat_id" : chat_id})
