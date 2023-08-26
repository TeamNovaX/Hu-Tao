from threading import RLock
from time import time

from ..database import *


usrdb = dbname["users"]

class Users():
    async def update_user(usrdb, name: str, username: str = None):
        if name != usrdb.user_info["name"] or username != usrdb.user_info["username"]:
            return await usrdb.update(
                {"_id": usrdb.user_id},
                {"username": username, "name": name},
            )
        return True

    async def delete_user(self):
        return await usrdb.delete_one({"_id": self.user_id})

    @staticmethod
    async def count_users():
        collection = usrdb
        return await collection.count()

    async def get_my_info(self):
        return await usrdb.user_info

    @staticmethod
    async def list_users():
        collection = usrdb
        return await collection.find_all()

    @staticmethod
    async def get_user_info(user_id: int or str):
            collection = usrdb
            if isinstance(user_id, int):
                curr = await collection.find_one({"_id": user_id})
            elif isinstance(user_id, str):
                curr = await collection.find_one({"username": user_id[1:]})
            else:
                curr = None

            if curr:
                return curr

            return {}


