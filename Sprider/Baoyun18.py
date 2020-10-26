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
		Products_Res_Data = json.loads(Detail_Res.text)
		return Products_Res_Data

	def run(self):
		subUserId = self.Login()
		current_page = 1
		while True:
			Products_List = self.Get_Products_Menu(subUserId, current_page)
			if(len(Products_List) > 0):
				Products_Iter = iter(Products_List)
				for Product_Dict in Products_Iter:
					planName = Product_Dict["planName"][0]
					tempId = Product_Dict["tempId"]
					productId = Product_Dict["productId"]
					# print(tempId, productId)
					Product_Details = self.Get_Product_Detail(tempId, productId)
					Product_Details_Content = Product_Details["content"] if "content" in Product_Details else {}
					for Product_Details_Content_Dict in iter(Product_Details_Content):
						requests_data = {
							"program_id" : self.program_id if self.program_id else 0,
							"product_id" : productId,
							"product_name": planName if planName else "unknown",
							"temp_id" : tempId,
							"payDesc" : Product_Details_Content_Dict["payDesc"],
							"insureDesc": Product_Details_Content_Dict["insureDesc"],
							"first_rate" : float(Product_Details_Content_Dict["firstRate"]),
							"second_rate" : float(Product_Details_Content_Dict["secondRate"])
						}
						res = requests.post(url = "http://106.12.160.222:8001/insert/Baoyun18", data = json.dumps(requests_data))
						# res = requests.post(url = "http://127.0.0.1:8001/insert/Baoyun18", data = json.dumps(requests_data))
					print(planName + ": 记录保存成功")
					# print(planName, Product_Detail)
				current_page += 1
				time.sleep(3)
			else:
				break


if __name__ == "__main__":
	pass