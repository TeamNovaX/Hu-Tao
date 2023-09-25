#MIT License
#Copyright (c) 2023, ©NovaNetworks

from async_pymongo import AsyncClient

from HuTao import DB_URL

DBNAME = "HUTAO"

mongo = AsyncClient(DB_URL)
dbname = mongo[DBNAME]
