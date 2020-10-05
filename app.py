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

mysqlmodule = MysqlModule()

@app.get("/test")
async def index(request:Request, searchType: int = None, page:int = None, program_id:int = None, product_id:int = None, product_key:str = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or ""
    }
    print("datadict in test: ")
    print(datadict)
    if searchType == 1 and program_id == 1000:
        #Baoyun18
        result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    elif searchType == 1 and program_id == 1001:
        # qixin18
        result_dict = mysqlmodule.GetDataFromQixin18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    elif searchType == 1 and program_id == 1002:
        # Niubao1000
        result_dict = mysqlmodule.GetDataFromNiubao100(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    elif searchType == 1 and program_id == 999:
        print("datadict in all program")
        # All Program
        print(datadict)
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    else:
        print("enter else")
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict})

@app.get("/test/search")
async def search(request:Request, searchType:int = None, page:int = None, program_id:int = None, product_key:str = None):
    datadict = {
        "searchType": searchType,
        "page": page,
        "program_id": program_id,
        "product_key": product_key 
    } 
    print("request_url: ")
    print(request.url)
    print(request.base_url)
    #Baoyun18
    if searchType == 1 and program_id == 1000:
        result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        if result_dict["success"] == False:
            print(result_dict["fail_reason"])
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        return ProductsList
    elif searchType == 1 and program_id == 1001:
        # qixin18
        pass
    elif searchType == 1 and program_id == 1002:
        # Niubao1000
        pass
    elif searchType == 2 and product_key is not None:
        # All Program
        pass
    else:
        pass

    
        
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8002)