import os
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os.path


# __file__ 就是本文件的名字
# 得到放置模板的目录
path = '{}/webapp/'.format(os.path.dirname(__file__))
templates = Jinja2Templates(directory=path)

app = FastAPI()
app.mount("/static", StaticFiles(directory=path), name="static")

@app.get("/test")
async def index(request: Request):
    ProductsData ={
        "program_id": 1001,
        "product_list": [
            {"product_name": "产品1", "details":[
                {"pyDesc":"30年缴费", "insureDesc":"终身","first_rate":"20%","second_rate":"30%"},
                {"pyDesc":"20年缴费", "insureDesc":"20年","first_rate":"10%","second_rate":"15%"},
                {"pyDesc":"10年缴费", "insureDesc":"10年","first_rate":"5%","second_rate":"10%"},
            ],"program_id": 1001},
            {"product_name": "产品2","details":[
                {"pyDesc":"3年缴费", "insureDesc":"终身","first_rate":"2%","second_rate":"30%"},
                {"pyDesc":"2年缴费", "insureDesc":"20年","first_rate":"1%","second_rate":"15%"},
                {"pyDesc":"1年缴费", "insureDesc":"10年","first_rate":"5%","second_rate":"10%"},
            ],"program_id": 1001},
            {"product_name": "产品2","details":[
                {"pyDesc":"3年缴费", "insureDesc":"终身","first_rate":"2%","second_rate":"30%"},
                {"pyDesc":"2年缴费", "insureDesc":"20年","first_rate":"1%","second_rate":"15%"},
                {"pyDesc":"1年缴费", "insureDesc":"10年","first_rate":"5%","second_rate":"10%"},
            ],"program_id": 1001},
            {"product_name": "产品2","details":[
                {"pyDesc":"3年缴费", "insureDesc":"终身","first_rate":"2%","second_rate":"30%"},
                {"pyDesc":"2年缴费", "insureDesc":"20年","first_rate":"1%","second_rate":"15%"},
                {"pyDesc":"1年缴费", "insureDesc":"10年","first_rate":"5%","second_rate":"10%"},
            ],"program_id": 1001},
            {"product_name": "产品2","details":[
                {"pyDesc":"3年缴费", "insureDesc":"终身","first_rate":"2%","second_rate":"30%"},
                {"pyDesc":"2年缴费", "insureDesc":"20年","first_rate":"1%","second_rate":"15%"},
                {"pyDesc":"1年缴费", "insureDesc":"10年","first_rate":"5%","second_rate":"10%"},
            ],"program_id": 1001}
            
        ]
    }
    return templates.TemplateResponse("index.html", {"request": request, "ProductsData": ProductsData})
    
if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8002)