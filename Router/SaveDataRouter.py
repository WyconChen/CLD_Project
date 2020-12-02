from fastapi import APIRouter
from .RequestModel.RequestModel import JsonDataModel
from DBHandler.DBHandler import DBHandler

SaveDataRouter = APIRouter()

@SaveDataRouter.post("/set_json_data_status_to_1/")
async def Set_Data_To_1():
    DBH = DBHandler()
    result = DBH.DelDataFrom_CLD_DATA()
    return {"result": result}

@SaveDataRouter.post("/save_json_data/")
async def Save_Data_To_DB(request_data: JsonDataModel):
    DBH = DBHandler()
    datadict = dict(request_data)
    result = DBH.SaveJsonDataToDB(datadict)
    return {"result": result}
