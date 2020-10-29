from fastapi import APIRouter
from .RequestModel.RequestModel import JsonDataModel
from DBHandler.DBHandler import DBHandler

SaveDataRouter = APIRouter()

@SaveDataRouter.post("/save_json_data/")
async def Save_Data_To_DB(request_data: JsonDataModel):
    datadict = dict(request_data)
    result = DBHandler.SaveJsonDataToDB(datadict)
    return {"result": result}
