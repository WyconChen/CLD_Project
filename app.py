import os
import uvicorn
import platform
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
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
    if searchType == 1 and program_id == 1000:
        #Baoyun18
        result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1001:
        # qixin18
        result_dict = mysqlmodule.GetDataFromQixin18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1002:
        # Niubao1000
        result_dict = mysqlmodule.GetDataFromNiubao100(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 999:
        # All Program
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1005:
        # Zhongbao
        result_dict = mysqlmodule.GetDataFromZhongbao(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
        # print(ProductsList)
        # return result_dict
    elif searchType == 1 and program_id == 1004:
        # Zhongbao
        result_dict = mysqlmodule.GetDataFromFengqi(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    else:
        print("enter else")
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict, "pageList":pageList, "total_num":total_num})

@app.get("/test/search")
async def search(request:Request, searchType:int = None, page:int = None, program_id:int = None, product_key:str = None, pageSize: int = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    if searchType == 1 and program_id == 1000:
        #Baoyun18
        result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1001:
        # qixin18
        result_dict = mysqlmodule.GetDataFromQixin18(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1002:
        # Niubao1000
        result_dict = mysqlmodule.GetDataFromNiubao100(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 999:
        # All Program
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    elif searchType == 1 and program_id == 1004:
        # All Program
        result_dict = mysqlmodule.GetDataFromFengqi(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
        return ProductsList
    elif searchType == 1 and program_id == 1005:
        # Zhongbao
        result_dict = mysqlmodule.GetDataFromZhongbao(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
        # print(ProductsList)
        return result_dict
    else:
        print("enter else")
        result_dict = mysqlmodule.GetDataFromAll(datadict)
        ProductsList = result_dict["result_list"] if result_dict["success"] else []
        total_num = result_dict["total_num"] if result_dict["success"] else 0
        pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict, "pageList":pageList, "total_num":total_num})

    
        
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8002)