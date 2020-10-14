# import os
# import uvicorn
# import platform
# from fastapi import FastAPI
# from starlette.requests import Request
# from starlette.staticfiles import StaticFiles
# from starlette.templating import Jinja2Templates
# from Api.Model.model import Baoyun18DataModel
# from Api.Func.MysqlModule import MysqlModule



# # __file__ 就是本文件的名字
# # 得到放置模板的目录
# if platform.system() == "Windows":
#     path = '{}/webapp/'.format(os.path.dirname(__file__))
# else:
#     path = './webapp/'
# templates = Jinja2Templates(directory=path)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory=path), name="static")

# # mysqlmodule = MysqlModule()

# @app.get("/test")
# async def index(request:Request, searchType: int = None, page:int = None, program_id:int = None, product_id:int = None, product_key:str = None):
#     datadict = {
#         "searchType": 1,
#         "page": page or 1,
#         "program_id": program_id or 1000,
#         "product_key": product_key or ""
#     } 
#     #Baoyun18
#     if searchType == 1 and program_id == 1000:
#         # result_dict = mysqlmodule.GetDataFromBaoyun18(datadict)
#         print(datadict)
#         ProductsList = []
#     elif searchType == 1 and program_id == 1001:
#         # qixin18
#         ProductsList = []
#     elif searchType == 1 and program_id == 1002:
#         # Niubao1000
#         ProductsList = []
#     elif searchType == 2 and product_key is not None:
#         # All Program
#         ProductsList = []
#     else:
#         ProductsList = []
#     return templates.TemplateResponse("index.html", {"request":request,"ProductsList": ProductsList, "DataDict":datadict})

# @app.get("/test/search")
# async def search(request:Request, searchType:int = None, page:int = None, program_id:int = None, product_key:str = None):
#     datadict = {
#         "searchType": 1,
#         "page": page or 1,
#         "program_id": program_id or 1000,
#         "product_key": product_key 
#     } 
#     return datadict
    
    
    
        
if __name__ == "__main__":
 	# uvicorn.run(app=app, host="0.0.0.0", port=8003)
#     import requests
#     import json
#     Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
#             "Cookie": r"beidoudata2015jssdkcross=%7B%22distinct_id%22%3A%22174a66293b63c-0637b0acb8b219-3d634d00-1049088-174a66293b7f8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22174a66293b63c-0637b0acb8b219-3d634d00-1049088-174a66293b7f8%22%7D; auth-tips=1; orderTips=true; acw_tc=2f6a1fae16018220592497901e4cc07a252e448a19e3a9e479f361ac4efb59; env=preview; qx_trip_pc_sid=s%3A7syvbD8geILNfN9FoAngSwuC6uLWcKH4.0clPe3QbUfqbTZ72eq5oo3PP%2FdixK%2FnDrihg%2Bl5sHXM; hz_guest_key=1HwfYz8BIHZ3oGHRCu79_1601778137707_1_0_0; hz_visit_key=4uJEkIBcsHZ27khLgY9x_1601822596509_6_1601822596509; hz_view_key=1HwfYz8BIHZ3oGHRCu793iUcH3xmdHZ2fnmmIu4C_1601822678723_https%253A%252F%252Fwww.qixin18.com%252Fgoods%253Fis_from_new_merchant_pc%253Dtrue"
#     }
#     Form_Data = {"productId": 104107, "planId": 128618}

#     url = "https://www.qixin18.com/goods/getPartnerProductFeeWithActivity"
#     res = requests.post(url = url, headers=Headers, data=Form_Data)
#     print(res.text)

        datadict = {'program_id': 1005, 'product_id': '1262588866298257411', 'product_name': '信泰如意尊终身寿险-上海版', 'clauseId': '202005251610000101', 'clauseName': '信泰如意尊终身寿险', 'extraType': 1, 'rateCodeDescView': '', 
'rateCode': 'SP', 'rateCodeDesc': '一次性缴纳', 'yearCode': 'SP', 'yearCodeDesc': '一次性缴纳', 'first_rate': 4.3, 'second_rate': 0.0, 'third_rate': 0.0, 'fourth_rate': 0.0, 'fifth_rate': 0.0}
        # sql = "INSERT INTO CLD_Zhongbao ({DataKeyList}) VALUES ({DataValuesList});"
        # DataKeyList = []
        # DataValueList = []
        # for key, value in datadict.items():
        #         keyStr = "`" + key + "`"
        #         if(type(value) == str):
        #            valueStr = "'" + value + "'"
        #         else:
        #            valueStr = str(value)
        #         DataKeyList.append(keyStr)
        #         DataValueList.append(valueStr)

        # # print(",".join(DataKeyList))
        # # print(",".join(DataValueList))
        # a = sql.format(DataKeyList=",".join(DataKeyList), DataValuesList=",".join(DataValueList))
        # print(a)
