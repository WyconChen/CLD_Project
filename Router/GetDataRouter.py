import os
import platform
from typing import Optional
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from DBHandler.DBHandler import DBHandler

GetDataRouter = APIRouter()


if platform.system() == "Windows":
    path = '{}/../webapp/'.format(os.path.dirname(__file__))
else:
    path = '{}/../webapp/'.format(os.path.dirname(__file__))
templates = Jinja2Templates(directory=path)

@GetDataRouter.get("/baoxian/")
async def BaoXianGetData(request:Request, searchType: Optional[int] = 1, page:int = None, program_id:int = None, product_key:str = None, pageSize:int = None):
    DBH = DBHandler()
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    product_list, total_num = DBH.GetJsonDataFromDB(datadict)
    pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("main.html", {"request":request,"ProductsList": product_list, "DataDict":datadict, "pageList":pageList, "total_num":total_num})

@GetDataRouter.get("/baoxian/test")
async def BaoXianGetData(request:Request, searchType: Optional[int] = 1, page:int = None, program_id:int = None, product_key:str = None, pageSize:int = None):
    DBH_TEST = DBHandler()
    datadict = {
        "searchType": 1,
        "page": page or 1,
        # program_id: 
        # 1000： BaoYun18
        # 1001: QiXin18
        # 1002: Niubao 100
        # 1004: FengQi
        # 1005: Zhongbao
        # 其他：ALL
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    product_list, total_num = DBH_TEST.GetJsonDataFromDB(datadict)
    pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    # return templates.TemplateResponse("index.html", {"request":request,"ProductsList": product_list, "DataDict":datadict, "pageList":pageList, "total_num":total_num})
    return product_list

@GetDataRouter.get("/v2/baoxian/")
async def BaoXianGetDataVersion_2(request:Request, searchType: Optional[int] = 1, page:int = None, program_id:int = None, product_key:str = None, pageSize:int = None):
    DBH = DBHandler()
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    product_list, total_num = DBH.GetJsonDataFromDB(datadict)
    pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("main_v2.html", {"request":request,"ProductsList": product_list, "DataDict":datadict, "pageList":pageList, "total_num":total_num})