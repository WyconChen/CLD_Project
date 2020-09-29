from typing import List
import requests
import json
import hashlib



class Niubao100:

    
    
    def __init__(self) -> None:
        self.loginURL = r"https://www.niubao100.com/user/login"
        self.user_name = "13539869933"
        self.password = "QWEqwe123"
        self.productList_url = "https://www.niubao100.com/item/pcListItem"
        self.productDetail_url = "https://www.niubao100.com/item/getItemCommList"
        self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
        self.Niubao_Session = requests.Session()
    
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
        item_id = Item_Dict["itemid"]
        item_name = Item_Dict["name"]
        DetailsList_Res = self.Niubao_Session.post(url = self.productDetail_url, headers = self.Headers,data = FormData)
        DetailsList_Dict = json.loads(DetailsList_Res.text) if DetailsList_Res.ok else {}
        if DetailsList_Dict:
            skus_list = DetailsList_Dict["data"]["skus"]
            for skus in iter(skus_list):
                result_dict = {"program_id":1003, "item_id": item_id, "item_name": item_name,"sku_str": None}
                result_dict["insuranceType"] = skus["insuranceType"] if "insuranceType" in skus else "unknown"
                result_dict["sku"] = skus["sku"] if "sku" in skus else 0.0
                print (type(result_dict["sku"]))
                if type(result_dict["sku"]) == str:
                    result_dict["sku_str"] = result_dict["sku"]
                    result_dict["sku"] = 0.0
                result_dict["paytime"] = skus["paytime"] if "paytime" in skus else "unknown"
                result_dict["savetime"] = skus["savetime"] if "savetime" in skus else "null"
                result_dict["insuredage"] = skus["insuredage"] if "insuredage" in skus else "null"
                result_dict["actratio"] = skus["actratio"] if "actratio" in skus else 0
                result_dict["y1"] = float(skus["y1"]) if "y1" in skus else 0.0
                result_dict["y2"] = float(skus["y2"]) if "y2" in skus else 0.0
                result_dict["y3"] = float(skus["y3"]) if "y3" in skus else 0.0
                result_dict["y4"] = float(skus["y4"]) if "y4" in skus else 0.0
                result_dict["y5"] = float(skus["y5"]) if "y5" in skus else 0.0
                # print(result_dict)
                res = requests.post(url="http://106.12.160.222:8001/insert/Niubao100", data=json.dumps(result_dict))

    def run(self) -> None:
        self.Login()
        page = 1
        while True:
            ProductList = self.getProductListItem(page=page)
            if len(ProductList) <= 0:
                break
            for ProductDict in iter(ProductList):
                self.getProductDetails(List[ProductDict])
            page += 1
            

if __name__ == "__main__":
    n = Niubao100()
    n.run()