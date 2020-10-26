import os
import platform
from typing import Optional
from fastapi import APIRouter
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from DBHandler.DBHandler import DBHandler

appRouter = APIRouter()

if platform.system() == "Windows":
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
else:
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
templates = Jinja2Templates(directory=path)

appRouter.mount("/static", StaticFiles(directory=path), name="static")

DBHandler = DBHandler()

@appRouter.get("/test")
async def App_Run(request:Request, searchType: Optional[int] = 1, page:int = None, program_id:int = None, product_id:int = None, product_key:str = None, pageSize:int = None):
    datadict = {
        "searchType": 1,
        "page": page or 1,
        "program_id": program_id or 999,
        "product_key": product_key or "",
        "pageSize": pageSize or 5
    }
    result_dict = DBHandler.GetDataFromDB(datadict)
    ProductsList = result_dict["result_list"] if result_dict["success"] else []
    total_num = result_dict["total_num"] if result_dict["success"] else 0
    pageList = [datadict["page"]-2, datadict["page"]-1, datadict["page"], datadict["page"]+1, datadict["page"]+2]
    return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict, "pageList":pageList, "total_num":total_num})

if __name__ == "__main__":
    print(os.path.dirname(__file__))