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

@app.get("/test")
async def index(request:Request, searchType: int = None, page:int = None, program_id:int = None, product_id:int = None, product_name:str = None):
    datadict = {
        "searchType": searchType,
        "page": page,
        "program_id": program_id,
        "product_id": product_id,
        "product_name": product_name
    }
    if searchType or page or program_id or product_key:
        print('enter step 1')
        mysqlmodule = MysqlModule()
        result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    else:
        print('enter step 2')
        ProductsList = []
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList})

@app.get("/test/search")
async def search(request:Request, searchType:int = None, page:int = None, program_id:int = None, product_key:str = None):
    datadict = {
        "searchType": searchType,
        "page": page,
        "program_id": program_id,
        "product_key": product_key 
    }
    mysqlmodule = MysqlModule()
    result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
    if result_dict["success"] == False:
        print(result_dict["fail_reason"])
    ProductsList = result_dict["result_list"] if result_dict["success"] else []
    return ProductsList
    
        
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8002)