from fastapi import APIRouter

SaveDataRouter = APIRouter()

@SaveDataRouter("/getdata/{}")
async def Save_Data_To_DB():
    pass