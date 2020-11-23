import requests
import json
import time

from requests.sessions import session

class ZhongBao:

    def __init__(self) -> None:
        self.login_api = "https://www.zhongbaounion.com/jwt/token"
        self.products_menu_api = "https://www.zhongbaounion.com/api/companyCommission/company/product/productList"
        self.product_detail_api = "https://www.zhongbaounion.com/api/companyCommission/company/commission/productRateDetailActive"
        self.proposal_url = "https://www.zhongbaounion.com/api/companyCommission/company/product/proposalUrl/list"
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
        print("Zhongbao Start...")

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

    def GetProposalUrl(self,product_name: str):
        formdata = {
            "agencyId": "1260127988355842048",
            "groupId": "1260126152177618944",
            "limit": 100,
            "orgId": "1260126149736534016",
            "page":1,
            "spuName": product_name
        }
        res = self.ZBSession.post(url=self.proposal_url, headers=self.Headers, data=json.dumps(formdata))
        ProductUrlData = json.loads(res.text)
        if res.ok and ProductUrlData["status"] == 200 and "data" in ProductUrlData:
            products_url_list = ProductUrlData["data"]["list"]
            return products_url_list
        else:
            return []
    
    def GetProductDetail(self, products_list: list):
        for productInfos in products_list:
            product_id = productInfos["productId"]
            productName = productInfos["productName"]
            formdata = {"memberId":"1260126152165036032","rateType":"2","productId":product_id,"tabType":"1","orgId":"1260126149736534016"}
            res = self.ZBSession.post(url=self.product_detail_api, headers=self.Headers, data=json.dumps(formdata))
            ProductData = json.loads(res.text) if res.ok else None
            if "data" in ProductData:
                ProductData["proposal_url"] = self.GetProposalUrl(productName)
                datadict = {}
                datadict["program_id"] = 1005
                datadict["product_id"] = product_id
                datadict["product_name"] = productName
                datadict["data"] = json.dumps(ProductData, ensure_ascii=False)
                datadict["proposal_url"] = self.GetProposalUrl(productName)
                ZBres = requests.post(url="http://106.12.160.222:8002/save_json_data/", data=json.dumps(datadict))
                result = json.loads(ZBres.text)
                if(result["result"] == False):
                    print(datadict["product_name"] + ": 保存失败")
            else:
                print(productName+ ": 该产品下暂无详细费率, 暂不作保存")
    def run(self):
        self.Login()
        page = 1
        while True:
            products_list = self.GetProductsMenu(page=page)
            # products_list = [{"productId": "1224601300852224002", "productName":"test"}]
            if len(products_list) > 0:
                self.GetProductDetail(products_list)
            else:
                break
            page += 1

if __name__ == "__main__":
    zb = ZhongBao()
    zb.run()