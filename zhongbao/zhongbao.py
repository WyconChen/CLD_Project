import requests
import json

from requests.sessions import session

class ZhongBao:

    def __init__(self) -> None:
        self.login_api = "https://www.zhongbaounion.com/jwt/token"
        self.products_menu_api = "https://www.zhongbaounion.com/api/companyCommission/company/product/productList"
        self.product_detail_api = "https://www.zhongbaounion.com/api/companyCommission/company/commission/productRateDetailActive"
        self.Headers = {               
                "Host":"www.zhongbaounion.com",
                "Connection":"keep-alive",
                "Content-Length":"127",
                "Accept":"application/json, text/plain, */*",
                "Origin":"https://www.zhongbaounion.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
                "Content-Type":"application/json;charset=UTF-8",
                "Referer":"https://www.zhongbaounion.com/grainbuds/",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.9",
                # "Cookie":"""accessId=31529010-52db-11e8-94ba-1b5a52d1a829; href=https%3A%2F%2Fwww.zhongbaounion.com%2Fgrainbuds%2F%23%2Flogin; pageViewNum=8; SESSION=MThhMTQzNzAtY2Y3ZC00M2NmLWIzOTgtY2UxN2FjODIyNjI5""",
                "Authorization":""
        }
        self.ZBSession = requests.session()

    def Login(self) -> None:
        login_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Connection": "keep-alive",
            "Content-Length": "237",
            "Content-Type": "application/json",
            "Host": "www.zhongbaounion.com",
            "Referer": "https://www.zhongbaounion.com/grainbuds/",
            "Origin": "https://www.zhongbaounion.com",
            # "Cookie": r"accessId=31529010-52db-11e8-94ba-1b5a52d1a829; qimo_seosource_31529010-52db-11e8-94ba-1b5a52d1a829=%E7%AB%99%E5%86%85; qimo_seokeywords_31529010-52db-11e8-94ba-1b5a52d1a829=; href=https%3A%2F%2Fwww.zhongbaounion.com%2Fgrainbuds%2F%23%2Flogin; pageViewNum=7"
        }
        password = "UYGf0U04dF/XVKrGphdbQi1TfvuRJSoS2UyZP7NUDiyJzrqakRpBVvtBRXVV+RKzuAcifsJDRqDo7ciBFn8RjPmVBVJKX8sJMps6psQ6ksXew43CTPFob6VEt+/mdrDuPDYdcTc6FwBHTS2ZVhmsTbqeYSGajSmAi8LTrUVuU5c="       
        formdata = {
            "password": password,
            "systemNo": "02",
            "tenantCode": "JB",
            "username":"JB"
        }
        res = self.ZBSession.post(url=self.login_api, headers=login_headers, data=json.dumps(formdata))
        resData = json.loads(res.text)
        if res.ok and resData["status"] == 200: 
            self.Headers["Authorization"] = "bearer" + resData["tokenInfo"]["access_token"]
            print("Login successfully")
        else:
            print("Login failed")
    
    def GetProductsMenu(self, page) -> list :
        formdata = {
            "insureCompanyId": "",
            "orgId": "1260126149736534016",
            "pageNum": page,
            "pageSize": 10,
            "productCateId": "",
            "productName": "",
            "productState": "1",
            "productType": "",
            "singleChoice": ""
        }
        res = self.ZBSession.post(url=self.products_menu_api, headers=self.Headers, data=json.dumps(formdata))
        ProductMenuData = json.loads(res.text)
        if res.ok and ProductMenuData["status"] == 200 and "data" in ProductMenuData:
            products_list = ProductMenuData["data"]["list"]
            return products_list
        else:
            return []

    
    def GetProductDetail(self, products_list: list):
        for productInfos in products_list:
            product_id = productInfos["productId"]
            productName = productInfos["productName"]
            formdata = {"memberId":"1260126152165036032","rateType":"2","productId":product_id,"tabType":"1","orgId":"1260126149736534016"}
            res = self.ZBSession.post(url=self.product_detail_api, headers=self.Headers, data=json.dumps(formdata))
            ProductData = json.loads(res.text) if res.ok else None
            commissionList = ProductData["data"]["rateDetail"]["commission"] if "data" in ProductData else None
            result_dict = {
                "program_id": 1005,
                "product_id": product_id,
                "product_name": productName
            }
            print(productName)
            if commissionList:
                for commission in commissionList:
                    result_dict["clauseId"] =  commission["clauseId"] if "clauseId" in commission else product_id
                    result_dict["clauseName"] = commission["clauseName"] if "clauseName" in commission else productName
                    result_dict["extraType"] = commission["extraType"]
                    feeList = commission["feeList"]
                    for fee in feeList:
                       result_dict["rateCodeDescView"] = fee["rateCodeDescView"] if "rateCodeDescView" in fee and fee["rateCodeDescView"] != "" else "-"
                       rateValueList = fee["rateValues"]
                       for rate in rateValueList:
                           result_dict["rateCode"] = rate["rateCode"]
                           result_dict["rateCodeDesc"] = rate["rateCodeDesc"] if "rateCodeDesc" in rate else "-"
                           result_dict["yearCode"] = rate["yearCode"] if rate["yearCode"] != "" else "-"
                           result_dict["yearCodeDesc"] = rate["yearCodeDesc"] if "yearCodeDesc" in rate and rate["yearCodeDesc"] != "" else "-"
                           result_dict["first_rate"] = float(rate["receivable"]["first"]) if "first" in rate["receivable"] else 0.0
                           result_dict["second_rate"] = float(rate["receivable"]["second"]) if "second" in rate["receivable"] else 0.0
                           result_dict["third_rate"] = float(rate["receivable"]["third"]) if "third" in rate["receivable"] else 0.0
                           result_dict["fourth_rate"] = float(rate["receivable"]["fourth"]) if "fourth" in rate["receivable"] else 0.0
                           result_dict["fifth_rate"] = float(rate["receivable"]["fifth"]) if "fifth" in rate["receivable"] else 0.0
                           res = requests.post(url="http://106.12.160.222:8001/insert/Zhongbao", data=json.dumps(result_dict))
                           resText = json.loads(res.text)
                           if resText["result"] == False:
                                print(productName + " have getProductDetails error_2: ")
                                print(resText)                          
            else:
                print("该产品下暂无详细费率, 暂不作保存")
    def run(self):
        self.Login()
        page = 1
        while True:
            products_list = self.GetProductsMenu(page=page)
            if len(products_list) > 0:
                self.GetProductDetail(products_list)
            else:
                break
            page += 1

if __name__ == "__main__":
    zb = ZhongBao()
    zb.run()