import uvicorn
from fastapi import FastAPI
from Api.Func.MysqlModule import MysqlModule
from Api.Model.model import ProgramModel, Baoyun18Model, Qixin18Model

app = FastAPI()

MysqlModule = MysqlModule()

# @app.post("/insert/Program")
# async def insertDataToProgram(request_data: ProgramModel):
#     DataDict = {
#     	  "program_id": ProgramModel.program_id,
#     	  "program_name": ProgramModel.program_name
#     }
#     mysqlFunc.insertDataToProgram(DataDict)

@app.post("/insert/Baoyun18")
async def insertDataToProgram(request_data: Baoyun18Model):
	# return {"result":"success"}
    DataDict = {
    	"program_id" : request_data.program_id,
    	"temp_id" : request_data.temp_id,
        "product_id" : request_data.product_id,
        "product_name": request_data.product_name.encode("utf-8"),
        "payDesc":request_data.payDesc.encode("utf-8"),
        "insureDesc":request_data.insureDesc.encode("utf-8"),
        "first_rate":request_data.first_rate,
        "second_rate":request_data.second_rate
    }
    result = MysqlModule.SaveDataToBaoyun18(DataDict)
    if result:
        return {"result":"success"}
    else:
        return {"result":"failed"}

@app.get("/getDataFrom/Baoyun18")
async def getDataFromBaoyun18():
    result = MysqlModule.GetDataFromBaoyun18()
    return {"result": result}

@app.post("/insert/Qixin18")
async def saveDataToQixin18(request_data: Qixin18Model):
    DataDict = {
        "program_id": request_data.program_id,
        "product_id": request_data.product_id,
        "product_name": request_data.product_name,
        "plan_Id": request_data.plan_Id,
        "company_id": request_data.company_id,
        "company_name": request_data.company_name,
        "isDetails": request_data.isDetails,
        "yearPolicyText": request_data.yearPolicyText,
        "insureAgeText": request_data.insureAgeText,
        "economyText": request_data.economyText,
        "feeRateList_1": request_data.feeRateList_1,
        "feeRateList_2": request_data.feeRateList_2
    }
    result = MysqlModule.SaveDataToQixin18(DataDict)
    if result:
        return {"result":"success"}
    else:
        return {"result":"failed"}

    
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8001)