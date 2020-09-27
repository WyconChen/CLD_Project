import requests
import json


class QiXin18:

    def __init__(self):
        self.userName = "13539869933"
        self.password = "QWEqwe123"
        self.Products_Api = "https://www.qixin18.com/goods/selectProductList"
        self.Product_Detail_Api = "https://www.qixin18.com/goods/getPartnerProductFeeWithActivity"
        
        self.QiXin_Session = requests.Session()
        self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                "Cookie": r"acw_tc=2f6a1fe016011933803435847e047c7aa36fce9ebbb8379af1fd93982f39b0; qx_trip_pc_sid=s%3APwRES3MHGJrg4nJ6ppXRRUJc74fQIItd.Gnn5Ze4Meb1FxfO4v0HsO29FNqdOXCgW26yR40hFy8g; hz_guest_key=2iqY9PhbGHZ3B3TUo1UO_1601193384304_1_0_0; env=preview; beidoudata2015jssdkcross=%7B%22distinct_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%7D; beidoujssdk_2015_cross_new_user=1; hz_visit_key=4rTAcnAzXHZ2KSJmGWhd_1601193384304_3_1601193384304; hz_view_key=2iqY9PhbGHZ3B3TUo1UO2qX8v62cdHZ3VX3KyB1Z_1601193398089_https%253A%252F%252Fwww.qixin18.com%252Fmerchant%252Fhome"
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
        # print("Products_Res.text: "+ Products_Res.text)
        Products_Res_Data = json.loads(Products_Res.text)
        Products_Data_List = Products_Res_Data["data"]["data"]
        print("page: " + str(page))
        return Products_Data_List

    def Get_Product_Details(self, Products_Data_Dict:dict):
        result_dict = {}
        result_dict["program_id"] = 1001
        result_dict["product_id"] = Products_Data_Dict["productId"]
        result_dict["product_name"] = Products_Data_Dict["productName"]
        result_dict["plan_Id"] = Products_Data_Dict["planId"]
        result_dict["company_id"] = Products_Data_Dict["companyId"]
        result_dict["company_name"] = Products_Data_Dict["companyName"]


        Form_Data = {"productId": result_dict["product_id"], "planId": result_dict["plan_Id"]}
        Details_Res = self.QiXin_Session.post(url=self.Product_Detail_Api, headers = self.Headers, data = Form_Data)
        Details_Res_Data = json.loads(Details_Res.text)
        # 判断是否存在data
        if "data" in Details_Res_Data:
            result_dict["isDetails"] = True
            Details_Res_List = Details_Res_Data["data"]["yearPolicyFeeDtoList"]
            Details_Intetor = iter(Details_Res_List)
            for Details_Dict in Details_Intetor:
                result_dict["yearPolicyText"] = Details_Dict["yearPolicyText"] if "yearPolicyText" in Details_Dict else "---"
                insureAgeFeeDtoList = Details_Dict["insureAgeFeeDtoList"]
                for insureAgeFeeDto in iter(insureAgeFeeDtoList):
                    result_dict["insureAgeText"] = insureAgeFeeDto["insureAgeText"] if "insureAgeText" in insureAgeFeeDto else "---"
                    partnerProductFeeItemDtoList = insureAgeFeeDto["partnerProductFeeItemDtoList"]
                    for partnerProductFeeItemDto in iter(partnerProductFeeItemDtoList):
                        result_dict["economyText"] = partnerProductFeeItemDto["economyText"] if "economyText" in partnerProductFeeItemDto else "unknown"
                        result_dict["feeRateList_1"] = float(partnerProductFeeItemDto["feeRateList"][0])
                        try:
                            result_dict["feeRateList_2"] = float(partnerProductFeeItemDto["feeRateList"][1]) if len(partnerProductFeeItemDto["feeRateList"])>1  else 0.0
                        except Exception as e:
                            result_dict["feeRateList_2"] = 0.0
                        # insert
                        # print(result_dict)
                        res = requests.post(url="http://106.12.160.222:8001/insert/Qixin18", data=json.dumps(result_dict))
            print(result_dict["product_name"] + ": 保存成功")
        else:
            result_dict["isDetails"] = False
            result_dict["yearPolicyText"] = "unknown"
            result_dict["insureAgeText"] = "unknown"
            result_dict["economyText"] = "unknown"
            result_dict["feeRateList_1"] = 0.0
            result_dict["feeRateList_2"] = 0.0
            # print(result_dict)
            res = requests.post(url="http://106.12.160.222:8001/insert/Qixin18", data=json.dumps(result_dict))
            print(result_dict["product_name"] + ": 保存成功 " )

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