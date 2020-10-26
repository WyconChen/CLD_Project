from fastapi import APIRouter

GetDataRouter = APIRouter()

@GetDataRouter.post("/savedata/{}")
async def Get_Data_From_DB():
    pass