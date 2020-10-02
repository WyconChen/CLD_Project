import os
import uvicorn
import platform
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from Api.Model.model import Baoyun18DataModel
from Api.Func.MysqlModule import MysqlModule



# __file__ 就是本文件的名字
# 得到放置模板的目录
if platform.system() == "Windows":
    path = '{}/webapp/'.format(os.path.dirname(__file__))
else:
    path = './webapp/'
templates = Jinja2Templates(directory=path)

app = FastAPI()
app.mount("/static", StaticFiles(directory=path), name="static")

# mysqlmodule = MysqlModule()

@app.get("/test")
async def index(request:Request, searchType: int = None, page:int = None, program_id:int = None, product_id:int = None, product_key:str = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 1000,
        "product_key": product_key or ""
    } 
    #Baoyun18
    if searchType == 1 and program_id == 1000:
        # result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        print(datadict)
        ProductsList = []
    elif searchType == 1 and program_id == 1001:
        # qixin18
        ProductsList = []
    elif searchType == 1 and program_id == 1002:
        # Niubao1000
        ProductsList = []
    elif searchType == 2 and product_key is not None:
        # All Program
        ProductsList = []
    else:
        ProductsList = []
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict})

@app.get("/test/search")
async def search(request:Request, searchType:int = None, page:int = None, program_id:int = None, product_key:str = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 1000,
        "product_key": product_key 
    } 
    return datadict
    
    
    
        
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8003)