#MIT License
#Copyright (c) 2023, ©NovaNetworks

import datetime
from HuTao.database import *

users = dbname["users"]
chats = dbname["chats"]

first_found_date = datetime.datetime.now()

async def add_user(user_id, username=None, chat_id=None, chat_title=None, Forwared=False):
    
    UserData = await users.find_one(
        {
            'user_id': user_id
        }
    )

    if UserData == None:
        UsersNums = await users.count_documents({})
        UsersIDs = UsersNums + 1
        
        if Forwared:
            UsersData = {
                '_id': UsersIDs,
                'user_id': user_id,
                'username': username,
                'chats': [],
                'first_found_date': first_found_date
                }
        else:
            UsersData = {
                '_id': UsersIDs,
                'user_id': user_id,
                'username': username,
                'chats': [
                    {   '_id': 1,
                        'chat_id': chat_id,
                        'chat_title': chat_title
                    }
                ],
                'first_found_date': first_found_date
                }


        await users.insert_one(
            UsersData
        )

    else:
        if username != UserData['username']:
            await users.update_one(
                {
                    'user_id': user_id
                },
                {
                    "$set": {
                        'username': username
                    }
                },
                upsert=True
            )

        GetUserChatList = []
        UsersChats = UserData['chats']

        if len(UsersChats) == 0:
            return

        for UserChat in UsersChats:
            GetUserChat = await UserChat.get('chat_id')
            GetUserChatList.append(GetUserChat)

        ChatsIDs = len(GetUserChatList) + 1
        if not chat_id in GetUserChatList:
            await users.update(
                {
                    'user_id': user_id
                },
                {
                '$push': {
                    'chats': {
                        '_id': ChatsIDs,
                        'chat_id': chat_id,
                        'chat_title': chat_title
                            }
                        }
                }

            )
    

async def add_chat(chat_id, chat_title):
    ChatData = await chats.find_one(
        {
            'chat_id': chat_id
        }
    )

    if ChatData == None:
        ChatsNums = await chats.count_documents({})
        ChatsIDs = ChatsNums + 1

        ChatData = {
            '_id': ChatsIDs,
            'chat_id': chat_id,
            'chat_title': chat_title,
            'first_found_date': first_found_date
            }
        
        await chats.insert_one(
            ChatData
        )
    else:
        await chats.update_one(
            {
                'chat_id': chat_id
            },
            {
                "$set": {
                    'chat_id': chat_id,
                    'chat_title': chat_title
                }
            },
            upsert=True
        )

async def GetAllChats() -> list:
    CHATS_LIST = []
    chatsList = await chats.find({})
    for chatData in chatsList:
        chat_id = chatData['chat_id']
        CHATS_LIST.append(chat_id)
    return CHATS_LIST
    

async def GetChatName(chat_id):
    ChatData = await chats.find_one(
        {
            'chat_id': chat_id
        }
    )
    if ChatData is not None:
        chat_title = ChatData['chat_title']
        return chat_title
    else:
        return None
    
async def get_user_info(user_id: int or str):
    if isinstance(user_id, int):
        cur = users.find_one({"user_id": user_id})
    elif isinstance(user_id, str):
        cur = users.find_one({"username": user_id})
    
    else:
        cur = None

    if cur:
        return cur
    
    return {}
    

