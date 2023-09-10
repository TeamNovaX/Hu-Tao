#MIT License
#Copyright (c) 2023, ©NovaNetworks

from HuTao.database import *

approvedb = dbname["approvals"] 

async def approve_user(chat_id : int,user_id : int ):
    r = await approvedb.update_one({"chat_id" : chat_id} , {"$addToSet" : {"user_ids" : user_id}} , upsert = True)
    return r.modified_count > 0


async def isApproved(chat_id : int,user_id : int) -> bool:
    return bool(await approvedb.find_one({"chat_id" : chat_id} , {"user_ids" : {"$in" : [user_id]}}))

async def disapprove_user(chat_id : int,user_id : int):
    r = await approvedb.update_one({"chat_id" : chat_id} , {"$pull" : {"user_ids" : user_id}})
    return r.modified_count > 0

async def approved_users(chat_id : int) -> list:
    chat = await approvedb.find_one({"chat_id" : chat_id}) 
    return chat["user_ids"] if chat else []    

