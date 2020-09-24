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
                "Cookie": r"beidoudata2015jssdkcross=%7B%22distinct_id%22%3A%22174a66293b63c-0637b0acb8b219-3d634d00-1049088-174a66293b7f8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22174a66293b63c-0637b0acb8b219-3d634d00-1049088-174a66293b7f8%22%7D; auth-tips=1; orderTips=true; acw_tc=2f6a1fb516008680168562803e0da090e7ca6c3d929026ff1472108400bb1d; env=preview; qx_trip_pc_sid=s%3AR8vMcFJH-MR69EOaJFBLotske7azffGK.Ps2on73bNqsABHU97SMIWLI%2FvXenaLtgftO%2BFbVwdL4; hz_guest_key=3oAiy3WyAHZ1gd2SrDlc_1600869511124_0_1048581_0; hz_visit_key=2ztiulyYtHZ3cmL4laqR_1600868039379_6_1600868039379; hz_view_key=3oAiy3WyAHZ1gd2SrDlc2CjlWcGhFHZ3mOr0f4Uc_1600869521140_https%253A%252F%252Fwww.qixin18.com%252Fgoods%253Fis_from_new_merchant_pc%253Dtrue"
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
                result_dict["yearPolicyText"] = Details_Dict["yearPolicyText"]
                insureAgeFeeDtoList = Details_Dict["insureAgeFeeDtoList"]
                for insureAgeFeeDto in iter(insureAgeFeeDtoList):
                    result_dict["insureAgeText"] = insureAgeFeeDto["insureAgeText"]
                    partnerProductFeeItemDtoList = insureAgeFeeDto["partnerProductFeeItemDtoList"]
                    for partnerProductFeeItemDto in iter(partnerProductFeeItemDtoList):
                        result_dict["economyText"] = partnerProductFeeItemDto["economyText"]
                        result_dict["feeRateList_1"] = float(partnerProductFeeItemDto["feeRateList"][0])
                        try:
                            result_dict["feeRateList_2"] = float(partnerProductFeeItemDto["feeRateList"][1]) if len(partnerProductFeeItemDto["feeRateList"])>1  else 0.0
                        except Exception as e:
                            result_dict["feeRateList_2"] = 0.0
                        # insert
                        # print(result_dict)
                        res = requests.post(url="http://127.0.0.1:8001/insert/Qixin18", data=json.dumps(result_dict))
                        print(res.text)
        else:
            result_dict["isDetails"] = False
            result_dict["yearPolicyText"] = "unknown"
            result_dict["insureAgeText"] = "unknown"
            result_dict["economyText"] = "unknown"
            result_dict["feeRateList_1"] = 0.0
            result_dict["feeRateList_2"] = 0.0
            # print(result_dict)
            res = requests.post(url="http://127.0.0.1:8001/insert/Qixin18", data=json.dumps(result_dict))
            print(res.text)
    def run(self):
        while True:
            page = 1
            Products_Data_List = self.Get_Produts_Menu(page = page)
            if len(Products_Data_List)>0:
                Products_Data_Iter = iter(Products_Data_List)
                for Products_Data_Dict in Products_Data_Iter:
                    self.Get_Product_Details(Products_Data_Dict)            
                break

if __name__ == "__main__":
    q = QiXin18()
    q.run()