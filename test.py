import os
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from Api.Model.model import Baoyun18DataModel
from Api.Func.MysqlModule import MysqlModule
import os.path


# __file__ 就是本文件的名字
# 得到放置模板的目录
path = '{}/webapp/'.format(os.path.dirname(__file__))
templates = Jinja2Templates(directory=path)

app = FastAPI()
app.mount("/static", StaticFiles(directory=path), name="static")

@app.get("/test")
async def index(request:Request, searchType: int = None, page:int = None, program_id:int = None, product_key:str = None):
    datadict = {
        "searchType": searchType,
        "page": page,
        "program_id": program_id,
        "product_key": product_key 
    }
    mysqlmodule = MysqlModule()
    result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
    ProductsList = result_dict["result_list"] if result_dict["success"] else []
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList})

@app.get("/test/search")
async def search(request:Request, page:int, program_id:int = None, product_key:str = None):
    datadict = {
        "page": page,
        "program_id": program_id,
        "product_key": product_key 
    }
    print(datadict)
    
        
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8002)