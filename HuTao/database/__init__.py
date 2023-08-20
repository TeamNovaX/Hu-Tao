from async_pymongo import AsyncClient

from HuTao import DB_URL

DBNAME = "HuTao"

mongo = AsyncClient(DB_URL)
dbname = mongo[DBNAME]
