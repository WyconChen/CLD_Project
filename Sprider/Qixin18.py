import requests
import json


class QiXin18:

    def __init__(self, cookies_str: str):
        self.userName = "13539869933"
        self.password = "QWEqwe123"
        self.Products_Api = "https://www.qixin18.com/goods/selectProductList"
        self.Product_Detail_Api = "https://www.qixin18.com/goods/getPartnerProductFeeWithActivity"
        
        self.QiXin_Session = requests.Session()
        self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                "Cookie": cookies_str
        }

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
        Products_Res = self.QiXin_Session.post(url=self.Products_Api, headers = self.Headers, data = Form_Data)
        Products_Res_Data = json.loads(Products_Res.text)
        Products_Data_List = Products_Res_Data["data"]["data"]
        return Products_Data_List

    def Get_Product_Details(self, Products_Data_Dict:dict):
        result_dict = {}
        result_dict["program_id"] = 1001
        result_dict["product_id"] = Products_Data_Dict["productId"]
        result_dict["product_name"] = Products_Data_Dict["productName"]
        plan_Id = Products_Data_Dict["planId"]
        # result_dict["company_id"] = Products_Data_Dict["companyId"]
        # result_dict["company_name"] = Products_Data_Dict["companyName"]
        Form_Data = {"productId": result_dict["product_id"], "planId": plan_Id}
        Details_Res = self.QiXin_Session.post(url=self.Product_Detail_Api, headers = self.Headers, data = Form_Data)
        Details_Res_Data = json.loads(Details_Res.text)
        # 判断是否存在data
        try:
            if "data" in Details_Res_Data:
                result_dict["data"] = Details_Res.text
                # for yearPolicyFeeDto in Details_Res_Data["data"]["yearPolicyFeeDtoList"]:
                #     result_dict["yearPolicyText"] = yearPolicyFeeDto["yearPolicyText"] if "yearPolicyText" in yearPolicyFeeDto and yearPolicyFeeDto["yearPolicyText"] is not None else "未知保单年度"
                #     if "insureAgeFeeDtoList" in yearPolicyFeeDto:
                #         for insureAgeFeeDto in yearPolicyFeeDto["insureAgeFeeDtoList"]:
                #             result_dict["insureAgeText"] = insureAgeFeeDto["insureAgeText"] if insureAgeFeeDto["insureAgeText"] else "未知缴费年限"
                #             for partnerProductFeeItem in insureAgeFeeDto["partnerProductFeeItemDtoList"]:
                #                 result_dict["economyText"] = partnerProductFeeItem["economyText"]
                #                 result_dict["feeRateList_1"] = float(partnerProductFeeItem["feeRateList"][0]) if partnerProductFeeItem["feeRateList"][0] is not None else 0.0
                #                 result_dict["feeRateList_2"] = float(partnerProductFeeItem["feeRateList"][1]) if len(partnerProductFeeItem["feeRateList"])>=2 and partnerProductFeeItem["feeRateList"][1] is not None else 0.0
                #                 res = requests.post(url="http://106.12.160.222:8001/insert/Qixin18", data=json.dumps(result_dict))
                #                 resText = json.loads(res.text)
                #                 if resText["result"] == "failed":
                #                     print(result_dict["product_name"] + "： 保存失败")
                res = requests.post(url="http://106.12.160.222:8002/save_json_data/", data=json.dumps(result_dict))
                result = json.loads(res.text)
                if(result["result"] == False):
                    print(result_dict["product_name"] + ": 保存失败")
            else:
                print(result_dict["product_name"] + "不存在detail数据, 暂不作保存")         
        except Exception as e:
            print("保存失败, 原因如下:")
            print(e)

    def run(self):
        page = 1
        while True:
            Products_Data_List = self.Get_Produts_Menu(page = page)
            if len(Products_Data_List)>0:
                Products_Data_Iter = iter(Products_Data_List)
                for Products_Data_Dict in Products_Data_Iter:
                    self.Get_Product_Details(Products_Data_Dict)            
                page += 1
            else:
                break

if __name__ == "__main__":
    q = QiXin18()
    q.run()