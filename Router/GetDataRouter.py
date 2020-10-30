from fastapi import APIRouter
import os
import platform
from typing import Optional
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from DBHandler.DBHandler import DBHandler

GetDataRouter = APIRouter()
DBHandler = DBHandler()

if platform.system() == "Windows":
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
else:
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
templates = Jinja2Templates(directory=path)

@GetDataRouter.get("/baoxian/")
async def App_Run(request:Request, searchType: Optional[int] = 1, page:int = None, program_id:int = None, product_key:str = None, pageSize:int = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    product_list, total_num = DBHandler.GetJsonDataFromDB(datadict)
    pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": product_list, "DataDict":datadict, "pageList":pageList, "total_num":total_num})

