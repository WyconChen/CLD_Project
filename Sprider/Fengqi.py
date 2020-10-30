import requests
import json
import time

class FengQi:

    def __init__(self) -> None:
        self.login_api = "https://www.fxyf99.com/master/user/login"
        self.products_list_api = "https://www.fxyf99.com/master/product/getProductList"
        self.product_detail_api = "https://www.fxyf99.com/master/product/read/commisson"
        self.Headers = {
            "Host": "www.fxyf99.com",
            "Connection": "keep-alive",
            "Content-Length": "71",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.fxyf99.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.QxSession = requests.session()

    def Login(self):
        formdata = {"account":"13539869933","password":"QWEqwe123","time":int(time.time()*1000)}
        res = self.QxSession.post(url=self.login_api, headers=self.Headers, data=json.dumps(formdata))
        # print(json.loads(res.text))
    
    def GetProductList(self) -> list:
        self.Login()
        formdata = {"asc":False,"orderBy":"mp.id","pageNum":1,"pageSize":9999,"status":"2","time":int(time.time()*1000)}
        res = self.QxSession.put(url=self.products_list_api, headers=self.Headers, data=json.dumps(formdata))
        if res.ok:
            resData = json.loads(res.text)
            if "data" in resData:
                products_list = resData["data"]
                return products_list
            else:
                print("获取产品列表失败")
                return []
        else:
            print("请求产品列表失败")
            return []        
    
    def GetProductDetail(self, products_list):
        
        if len(products_list) <= 0:
            print("products_list为空")
        else:
            for productInfo in products_list:
                product_id = productInfo["id"]
                product_name = productInfo["productName"]
                formdata = {"productId":product_id, "time":int(time.time()*1000)}
                res = self.QxSession.put(url=self.product_detail_api, headers=self.Headers, data=json.dumps(formdata))
                if res.ok:
                    resData = json.loads(res.text)
                    if "data" in resData:
                        datadict = {}
                        datadict["program_id"] = 1004
                        datadict["product_id"] = product_id
                        datadict["product_name"] = product_name
                        datadict["data"] = res.text
                        FQresult = requests.post(url="http://106.12.160.222:8002/save_json_data/", data=json.dumps(datadict))
                        result = json.loads(FQresult.text)
                        if(result["result"] == False):
                            print(datadict["product_name"] + ": 保存失败")
                        # infosList = resData["data"]["list"]
                        # if len(infosList) > 0:
                        #     result_dict ={"program_id": 1004, "product_id": int(product_id[-1:-8:-1]), "product_name":product_name,
                        #     "commission_1": "-", "detail_id_1": "0", "payTerm_1": "-", "subsidyCommission_1": "-", 
                        #     "commission_2": "-", "detail_id_2": "0", "payTerm_2": "-", "subsidyCommission_2": "-", 
                        #     "commission_3": "-", "detail_id_3": "0", "payTerm_3": "-", "subsidyCommission_3": "-", 
                        #     "commission_4": "-", "detail_id_4": "0", "payTerm_4": "-", "subsidyCommission_4": "-", 
                        #     "commission_5": "-", "detail_id_5": "0", "payTerm_5": "-", "subsidyCommission_5": "-",
                        #     "commission_6": "-", "detail_id_6": "0", "payTerm_6": "-", "subsidyCommission_6": "-"
                        #     }
                        #     for commission_dict in infosList:
                        #         result_dict["productGrade"] = commission_dict["productGrade"] if "productGrade" in commission_dict and commission_dict["productGrade"] != "" else "-"
                        #         result_dict["productGradeId"] = commission_dict["productGradeId"] if commission_dict["productGradeId"] is not None else 0
                        #         commission_list = commission_dict["commissionList"]
                        #         for commissions in commission_list:
                        #             result_dict["curBack"] = int(commissions["curBack"]) if commissions["curBack"] != "" else 1
                        #             detail_no = 1
                        #             for com_detail in commissions["commissions"]:
                        #                 result_dict["commission_" + str(detail_no)] = com_detail["commission"] if "commission" in com_detail and com_detail["commission"] != "" else "-"
                        #                 result_dict["detail_id_" + str(detail_no)] = com_detail["id"] if com_detail["id"] is not None else "0"
                        #                 result_dict["payTerm_" + str(detail_no)] = com_detail["payTerm"] if "payTerm" in com_detail and com_detail["payTerm"] != "" else "-"
                        #                 result_dict["subsidyCommission_" + str(detail_no)] = com_detail["subsidyCommission"] if "subsidyCommission" in com_detail and com_detail["subsidyCommission"] != "" else "-"
                        #                 if detail_no > 7:
                        #                     break
                        #                 else:
                        #                     detail_no += 1
                        #             # print(result_dict)
                        #             res = requests.post(url="http://106.12.160.222:8001/insert/Fengqi", data=json.dumps(result_dict))
                        #             resText = json.loads(res.text)
                        #             if resText["result"] == False:
                        #                     print(product_name + " have getProductDetails error_2: ")
                        #                     print(resText) 

    def run(self):
        self.Login()
        product_list = self.GetProductList()
        # product_list = [{"id": '1305340737299742720', "productName":"test"}]
        self.GetProductDetail(product_list)



if __name__ == "__main__":
    F = FengQi()
    # F.Login()
    F.run()