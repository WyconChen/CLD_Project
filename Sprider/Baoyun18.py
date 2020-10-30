import requests
import json
import time

class BaoYun18:

	def __init__(self):

		self.program_id = 1000

		# User Info
		self.userName = "13539869933"
		self.password = "QWEqwe123"

		# Login Api
		self.Login_Api = "https://api.baoyun18.com/cs/login.json"
		self.Login_Type = "account"

		# Products Menu
		self.Products_Menu_Api = "https://api.baoyun18.com/cloud/commoditys.json"

		# Product_Detail
		self.Product_Detai_Api = "https://api.baoyun18.com/cloud/hoverFeeList.json"

		self.Baoyun_Session = requests.Session();
		self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}

	def Login(self):
		Login_PayLoad = {"userName": self.userName, "password": self.password, "isSend": "false", "ticket": "", "type": self.Login_Type}
		Login_Res = self.Baoyun_Session.post(url=self.Login_Api, headers = self.Headers, data = Login_PayLoad)
		Login_Res_Data = json.loads(Login_Res.text)
		subUserId = Login_Res_Data["content"]["userId"]
		return subUserId

	def Get_Products_Menu(self, subUserId, current_page):
		Request_Payloads = {"subUserId": subUserId, "commodityName": "", "commodityTypeCode": "all", "pageSize": 5, "currentPage": current_page}
		Products_Res = self.Baoyun_Session.post(url = self.Products_Menu_Api, headers = self.Headers, data = Request_Payloads)
		Products_Res_Data = json.loads(Products_Res.text)
		Products_List = Products_Res_Data["content"]["list"]
		return Products_List

	def Get_Product_Detail(self, tempId, productId):
		Request_Payloads = {"tempId": tempId, "productId": str(productId)}
		Detail_Res = self.Baoyun_Session.post(url = self.Product_Detai_Api, headers = self.Headers, data = Request_Payloads)
		Products_Res_Data = Detail_Res.text
		return Products_Res_Data

	def run(self):
		subUserId = self.Login()
		current_page = 1
		while True:
			Products_List = self.Get_Products_Menu(subUserId, current_page)
			if(len(Products_List) > 0):
				Products_Iter = iter(Products_List)
				for Product_Dict in Products_Iter:
					datadict = {"program_id": 1000}
					datadict["product_name"] =  Product_Dict["commodityName"]
					productIdArr = Product_Dict["productIdArr"]
					#  横琴人寿嘉贝保少儿重疾保险
					for product_id in productIdArr:
						tempId = Product_Dict["tempId"]
						datadict["product_id"] = product_id
						if Product_Dict["planName"][productIdArr.index(product_id)] != datadict["product_name"]:
							datadict["product_name"] = datadict["product_name"] + " - " + Product_Dict["planName"][productIdArr.index(product_id)]
						Product_Details = self.Get_Product_Detail(tempId, product_id)
						datadict["data"] = Product_Details
						res = requests.post(url="http://106.12.160.222:8002/save_json_data/", data=json.dumps(datadict))
						result = json.loads(res.text)
						if(result["result"] == False):
							print(datadict["product_name"] + ": 保存失败")
				current_page += 1
				time.sleep(1)
			else:
				break