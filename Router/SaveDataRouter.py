from fastapi import APIRouter

SaveDataRouter = APIRouter()

@SaveDataRouter.post("/getdata/{}")
async def Save_Data_To_DB():
    pass