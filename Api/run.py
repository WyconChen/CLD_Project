from fastapi import FastAPI
from Func.mysqlFunc import mysqlFunc
from Model.model import ProgramModel, Baoyun18Model

import json

app = FastAPI()

mysqlFunc = mysqlFunc()

@app.post("/insert/Program")
async def insertDataToProgram(request_data: ProgramModel):
    DataDict = json.loads(request_data)
    mysqlFunc.insertDataToProgram(DataDict)

@app.post("/insert/Baoyun18")
async def insertDataToProgram(request_data: Baoyun18Model):
    DataDict = json.loads(request_data)
    mysqlFunc.insertDataToBaiyun18(DataDict)