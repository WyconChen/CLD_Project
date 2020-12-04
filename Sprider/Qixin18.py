import requests
import json
import os

class QiXin18:

    def __init__(self):
        self.userName = "13539869933"
        self.password = "QWEqwe123"
        self.Login_Api = "https://www.qixin18.com/api/member/fmp/member/login?md=0.950482088046269"
        self.Products_Api = "https://www.qixin18.com/goods/selectProductList"
        self.Product_Detail_Api = "https://www.qixin18.com/goods/getPartnerProductFeeWithActivity"
        self.cookies_str = ""
        self.read_cookies()
        self.QiXin_Session = requests.Session()
        self.Headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }

    def Login(self):
        print("Qixin18 login...")
        Login_PayLoads = {"avoidLanding":"true","mobile":"13539869933","password":"QWEqwe123","tenantId":0,"verifyCode": "%7B%22a%22%3A%22FFFF000000000176F978%22%2C%22c%22%3A%221606979819631%3A0.262090909313194%22%2C%22d%22%3A%22nvc_login%22%2C%22h%22%3A%7B%22key1%22%3A%22code0%22%2C%22nvcCode%22%3A400%2C%22umidToken%22%3A%22T2gAp5coARA6DA64KbuoxijYKcSfx4nMMTgw9OO5FWqlJTQkuhNIRANtGMgC8seCJJXU7URlCh9neK9ZwtKL5mPD%22%7D%2C%22j%22%3A%7B%22test%22%3A1%7D%2C%22b%22%3A%22137%23hsB9hE9oUxqZpJVYYc2rMxJDIQikvfHs477LcWKB3j0BjRvRjh63FWkiG6IGBp3q6hXO1TeKhIUAZj1N1XJ8xLjjJzkU3fqyO5JWlGT7Q5dUtBQTL0%2FF4iCcm62wqmPKCgRMna06pVkpRj6sz8dgcGF6fs9CFKvGC8NJPYaWR9KAmapqFuoiU5RhUM%2FHxqwQt04honyRfTF7V8LpIm34nCKv%2FE7UewmeXSUml5BzE0xGq9mEsA0WXYNFfcMaY1vLGs6Yr7tcej1QwCXIV%2FEk8R15oGSvOFp55Zb02Nf1he1fjxR3yk%2BCqXiM%2FmMTaeOE6ttTk2M3VZ6V28Vw0PFMxUx6G%2F3z7aYwco3M8SM9uoL94XmqY4hPulzAtVLa3pJivDkeMKTaU1Qi%2B36DAAKmIt%2FPrJzDeSXInQAEAwhB6sQmo02V8VVhpjD7PqomNs22WDogYvAIaKUpXLtJOnigeosUrzL4izKoG6kkf03L6C%2FXaKQekgC6VAstwGulwI%2FqZLSQM1hoMgaMgmWerSVJV%2B%2FMg0RJQInd%2BaId9OrByLLvCkDwY12AY62jevDMkZ3AaUYmW2imYykdqX%2F2XG5yNlpkAx2dxxQW1pKtjRHVMAdgNuUWAP2k5vNCSscCnw%2FHX7puPFmopwsdFrE33d5spCqeXp%2BF2rAnGM3mGdzS4GfVp0R5Hd8ctGOt1qOsaeiCJskQtl0F9OPLK0vaSSBH7HGcC1OzjcV7wiXevCLMmNIrtCo2Agn%2BNrks5yvyoWPA%2FNXMOu13QAQ9L0h%2Fpa81IlFQ3AUoEqMKHUA6wlVADZC7lHKArYIKa%2BDUJZN2%2FCefyNooXQ%2FXenF2zaGgOm2zo7KLQfThFU8yMS%2Fuib1wEBf%2FWalmYNYfNiwB%2FyCuwsIhoMNsoOW6R2aeMxW%2BAp6Lqu01Iums6CwBViIBHxJKlPbGYd1M5Yt8CAfYG9xA6uKkVbdx7qBXjFRpADq1Azpenad45sQKvFaOTjfkbETaDCjGoeUZncOqn0ZzOGzZwGKEbY5e8grT4s4G%2BUAPThzXI6Ajwk8fco4AehZHOSsoFn%2BDjw2OR%2F%2BjYTUx1lg8pQyUQeRSjhdVFR2m1IEi%2BieEYTJx1qgypCGG%2BIXn%2BGDVpRUc1Aey%2BcGVYSS8TKcuktimLefJ%2BZDVpRJc1Keb0XiVYSUSplM8pIGj6IXH%2B6ZppkUm1AEi%2BXpVYTUx1lXHppimLenJ%2BGXppRJc1Iei%2BVIUxRkYiBqXEnTm%2BZq%2B6P8giLsIWvV7Vq76ZFuJKL1a5qXRN0bAwGTCB2a6ZZsRYbe6dCxTDAVJ8y3A3sbM3cn5U0kCsr2cMaNFDK18OFOJq6ugnzbce6gJxPFUulgleiJtyRc1X%2FWsNHjPCxBFblL%2BVo9mw3HDZdNvlmkXBau4gMZaPPzzKEks9zv7lwqGwMVEM0Jryarb%2F7gKo%2FIPm03SovzWNd%2FvKXUkMQE94S1MPNvlT9yM2K%2FOUnetWpDw6RhLeNCEFuyXUjls2yNVkebnKY25j49HO2thDm1f7pA%3D%22%2C%22e%22%3A%22XFqpV5C44hyAehVusnRgKD86dm2BroiIsaIs5N2t43nrAksQ67n_upaBc0dhwjhlR1jW4I7aGbMDI5W7OSFnodFMCtVLDFKzAEBhPYcSUnVaEHOEr6ZMz1BWZHaiuscrgXuwer0toy_sPQhGzpHhjJoHQdVHGWGHOcNKu25dGVl7EtMkMSX59E6Lcd2EKOX8%22%7D"}
        Login_Res = self.QiXin_Session.post(url = self.Login_Api, headers = self.Headers,  data = json.dumps(Login_PayLoads))
        if Login_Res.ok:
            Login_Data = json.loads(Login_Res.text)
            if Login_Data["success"]:
                print("Qixin Login successfully...")
                return self
            else:
                print("Qixin Login 失败...")

    def read_cookies(self):
        filepath = os.path.dirname(__file__) + r"/Qixin18_Cookies.txt"
        with open(filepath, 'r') as f:
            self.cookies_str = f.read()

    def Get_Produts_Menu(self, page:int) -> list:
        Form_Data = {
            "firstCategoryId": "",
            "secondCategoryId": "",
            "keyWords": "",
            "order": 6,
            "sortType": 0,
            "type": 0,
            "planStatus": 0,
            "productStatusList[]": 1,
            "returnProductType": 2,
            "pageIndex": page,
            "pageSize": 5,
            "dataType": 1,
            "isNeedMediaStatistics": "true",
            "isNeedMediaTagInfo": "true",
            "needFee": "true",
            "srcFromMobile": "false"
        }
        Menu_Headers = {
            "Referer": "https://www.qixin18.com/goods?is_from_new_merchant_pc=true",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Referer": "https://www.qixin18.com/goods?is_from_new_merchant_pc=true",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "traceparent": "00-732219d9981b6adc44844bbeed02843e-132dba9f68120766-01",
            "Host": "www.qixin18.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Cookie": "env=preview; qx_trip_pc_sid=s%3A-LTclYqyFwl3XX1uXP55T_t8UTKmDHOu.4yETXALmFfE3S%2Bx1z0gJ%2Fjrm1FQ9%2FHKfkB3F1R7r9ew; fmpUid=gOes4hhMoPuuxUlWk_9GhmLKhGn22fnckPVMSBDuUhU&6775&98IWvNfA8De3gBLy012QH1; acw_tc=2f6a1fd616069845095241895e8bd427076002008b2eff5d8a7456641b837e"
        }
        Products_Res = self.QiXin_Session.post(url=self.Products_Api, headers=Menu_Headers, data = json.dumps(Form_Data))
        Products_Res_Data = json.loads(Products_Res.text)
        Products_Data_List = Products_Res_Data["data"]["data"]
        return Products_Data_List

    def Get_Product_Details(self, Products_Data_Dict:dict):
        detailHeaders = {
            "Cookie":"env=preview; qx_trip_pc_sid=s%3A-LTclYqyFwl3XX1uXP55T_t8UTKmDHOu.4yETXALmFfE3S%2Bx1z0gJ%2Fjrm1FQ9%2FHKfkB3F1R7r9ew; fmpUid=gOes4hhMoPuuxUlWk_9GhmLKhGn22fnckPVMSBDuUhU&6775&98IWvNfA8De3gBLy012QH1; acw_tc=2f6a1fd616069845095241895e8bd427076002008b2eff5d8a7456641b837e",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        result_dict = {}
        result_dict["program_id"] = 1001
        result_dict["product_id"] = Products_Data_Dict["productId"]
        result_dict["product_name"] = Products_Data_Dict["productName"]
        plan_Id = Products_Data_Dict["planId"]
        # result_dict["company_id"] = Products_Data_Dict["companyId"]
        # result_dict["company_name"] = Products_Data_Dict["companyName"]
        Form_Data = {"productId": result_dict["product_id"], "planId": plan_Id}
        Details_Res = self.QiXin_Session.post(url=self.Product_Detail_Api, headers = detailHeaders, data = json.dumps(Form_Data))
        print(Details_Res.text)
        Details_Res_Data = json.loads(Details_Res.text)
        # 判断是否存在data
        try:
            if "data" in Details_Res_Data:
                result_dict["data"] = Details_Res.text
                print(result_dict["data"])
                # res = requests.post(url="http://120.25.103.152:8002/save_json_data/", data=json.dumps(result_dict))
                # result = json.loads(res.text)
                # if(result["result"] == False):
                #     print(result_dict["product_name"] + ": 保存失败")
            else:
                print(result_dict["product_name"] + "不存在detail数据, 暂不作保存")         
        except Exception as e:
            print("保存失败, 原因如下:")
            print(e)

    def run(self):
        self.Login()
        page = 1
        while True:
            Products_Data_List = self.Get_Produts_Menu(page = page)
            if len(Products_Data_List)>0:
                Products_Data_Iter = iter(Products_Data_List)
                for Products_Data_Dict in Products_Data_Iter:
                    self.Get_Product_Details(Products_Data_Dict)            
                page += 1
                break
            else:
                break

if __name__ == "__main__":
    q = QiXin18()
    q.run()