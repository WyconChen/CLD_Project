import uvicorn
from fastapi import FastAPI
from Func.mysqlFunc import mysqlFunc
from Model.model import ProgramModel, Baoyun18Model

import json

app = FastAPI()

mysqlFunc = mysqlFunc()

@app.post("/insert/Program")
async def insertDataToProgram(request_data: ProgramModel):
    DataDict = {
    	  "program_id": ProgramModel.program_id
    	  "program_name": ProgramModel.program_name
    }
    mysqlFunc.insertDataToProgram(DataDict)

@app.post("/insert/Baoyun18")
async def insertDataToProgram(request_data: Baoyun18Model):
	# return {"result":"success"}
    DataDict = {
    	"program_id" : request_data.program_id,
    	"temp_id" : request_data.temp_id,
        "product_id" : request_data.product_id,
        "product_name": request_data.product_name,
        "payDesc":request_data.payDesc,
        "insureDesc":request_data.insureDesc,
        "first_rate":request_data.first_rate,
        "second_rate":request_data.second_rate
    }
    mysqlFunc.insertDataToBaiyun18(DataDict)


if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8001)