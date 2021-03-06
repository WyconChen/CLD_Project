import hashlib
import json
import sys
import requests


class Niubao100:

    
    
    def __init__(self) -> None:
        self.loginURL = r"https://www.niubao100.com/user/login"
        self.user_name = "13539869933"
        self.password = "QWEqwe123qwe"
        self.productList_url = "https://www.niubao100.com/item/pcListItem"
        self.productDetail_url = "https://www.niubao100.com/item/getItemCommList"
        self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
        self.Niubao_Session = requests.Session()
        print("Niubao100 Start...")
    
    def Login(self):
        md5_passowrd= hashlib.md5(self.password.encode()).hexdigest()
        FormData = {
            "password": md5_passowrd,
            "mobile": "13539869933"
        }
        res = self.Niubao_Session.post(url = self.loginURL, headers = self.Headers, data = FormData)
    
    def getProductListItem(self, page):
        FormData = {
            "page": page,
            "pageSize": 30,
            "isCollect": 0,
            "itemName": "",
            "sortType": 0,
            "insuranceType":""
        }
        ProductList_Res = self.Niubao_Session.post(url = self.productList_url, headers = self.Headers,data = FormData)
        ProductList_Data = json.loads(ProductList_Res.text)
        Item_List  = ProductList_Data["data"]["items"] if "data" in ProductList_Data else []
        return Item_List
    
    def getProductDetails(self, Item_Dict):
        product_id = Item_Dict["itemid"]
        product_name = Item_Dict["name"]
        program_id = 1002
        FormData = {"itemId": product_id}
        DetailsList_Res = self.Niubao_Session.post(url = self.productDetail_url, headers = self.Headers,data = FormData)
        DetailsList_Dict = json.loads(DetailsList_Res.text) if DetailsList_Res.ok else {}
        if DetailsList_Dict:
            if "data" in DetailsList_Dict:
                datadict = {}
                datadict["program_id"] = program_id
                datadict["product_id"] = product_id
                datadict["product_name"] = product_name
                if "url" in Item_Dict:
                    DetailsList_Dict["url"] = Item_Dict["url"]
                else:
                    DetailsList_Dict["url"] = ""
                # print(DetailsList_Dict)
                datadict["data"] = json.dumps(DetailsList_Dict, ensure_ascii=False)
                # print(datadict["data"])
                # sys.exit(0)
                res = requests.post(url="http://120.25.103.152:8002/save_json_data/", data=json.dumps(datadict))
                result = json.loads(res.text)
                if(result["result"] == False):
                    print(datadict["product_name"] + ": 保存失败")
                # Type = 1 if "version" in DetailsList_Dict["data"]["skus"][0] else 2
                # # [version, ratio, renew_ratio] 
                # try:
                #     if Type == 1:
                #         for sku in DetailsList_Dict["data"]["skus"]:
                #             result_dict = {"program_id":1002, "product_id": product_id, "product_name": product_name, "Type": Type}
                #             result_dict["version"] = sku["version"] if sku["version"] != "" else "---"
                #             result_dict["ratio"] = sku["ratio"]
                #             result_dict["renew_ratio"] = sku["renew_ratio"]
                #             result_dict["insuranceType"] = ""
                #             result_dict["paytime"] = ""
                #             result_dict["savetime"] = ""
                #             result_dict["actratio"] = ""
                #             result_dict["y1"] = 0.0
                #             result_dict["y2"] = 0.0
                #             result_dict["y3"] = 0.0
                #             result_dict["y4"] = 0.0
                #             result_dict["y5"] = 0.0
                #             # print(result_dict)
                #             res = requests.post(url="http://106.12.160.222:8001/insert/Niubao100", data=json.dumps(result_dict))
                #             resText = json.loads(res.text)
                #             if resText["result"] == False:
                #                 print(product_name + " have getProductDetails error_3: ")
                #                 print(resText)
                #     # [insuranceType, paytime, savetime....y1, y2, y3, y4, y5]
                #     else:
                #         for skus in DetailsList_Dict["data"]["skus"]:
                #             result_dict = {"program_id":1002, "product_id": product_id, "product_name": product_name, "Type": Type}
                #             result_dict["insuranceType"] = skus["insuranceType"] if "insuranceType" in skus else "unknown"
                #             result_dict["paytime"] = skus["paytime"] if "paytime" in skus and skus["paytime"] is not None else "unknown"
                #             result_dict["savetime"] = skus["savetime"] if "savetime" in skus and skus["savetime"] is not None else "---"
                #             result_dict["actratio"] = float(skus["actratio"]) if skus["actratio"] is not None else 0.0
                #             result_dict["y1"] = float(skus["y1"]) if "y1" in skus else 0.0
                #             result_dict["y2"] = float(skus["y2"]) if "y2" in skus else 0.0
                #             result_dict["y3"] = float(skus["y3"]) if "y3" in skus else 0.0
                #             result_dict["y4"] = float(skus["y4"]) if "y4" in skus else 0.0 
                #             result_dict["y5"] = float(skus["y5"]) if "y5" in skus else 0.0
                #             result_dict["version"] = ""
                #             result_dict["ratio"] = ""
                #             result_dict["renew_ratio"] = ""
                #             # print(result_dict)
                #             res = requests.post(url="http://106.12.160.222:8001/insert/Niubao100", data=json.dumps(result_dict))
                #             resText = json.loads(res.text)
                #             if resText["result"] == False:
                #                 print(product_name + " have getProductDetails error_2: ")
                #                 print(resText)
                # except Exception as e:
                #     print(product_name + " have getProductDetails error_1: ")
                #     print(e)
            else:
                print(product_name + ": 没有detail数据, 不作保存")

    def run(self) -> None:
        self.Login()
        page = 1
        while True:
            ProductList = self.getProductListItem(page=page)
            if len(ProductList) <= 0:
                break
            for ProductDict in iter(ProductList):
                self.getProductDetails(ProductDict)
            page += 1
            

if __name__ == "__main__":
    n = Niubao100()
    n.run()
