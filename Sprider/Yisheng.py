import time
import xlrd
import requests
import json
import os

class Yisheng:

    def __init__(self, file_name, sheet_name) -> None:
        self.program_id = 1003
        self.userName = "13539869933"
        self.password = "QWEqwe123"
        self.login_api = "http://www.inswindow.com/login/userLogin.shtml"
        self.product_menu_api = "http://www.inswindow.com/myproduct/productListShowAjax.shtml"
        self.Yisheng_Session = requests.Session()
        self.Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.total_data_list = []


    def __Excel_Handler(self):
        # print(os.path.dirname(__file__))
        file_path = "{file_path}/Files/{file_name}".format(file_path = os.path.dirname(__file__), file_name = self.file_name)
        data = xlrd.open_workbook(file_path)
        table = data.sheets()[0]
        nrows = table.nrows  #获取该sheet中的有效行数
        # 474 行
        product_name = "first name"
        current_product = ""
        current_period = ""
        current_payment = ""
        id_index = 1
        datadict = {}
        datadict["data"] = {}
        for row_index in range(1, nrows):
            detail_list = []
            current_row_list = table.row_values(row_index)
            type_cell = current_row_list[0]
            product_name_cell = current_row_list[1]
            if not product_name or row_index == 1:
                product_name = product_name_cell
            period_cell = current_row_list[2]
            # print(period_cell)
            payment_cell = current_row_list[3]
            # 当类型 - 缴费年限都为空时，当前产品结束，重设记录参数
            if period_cell and product_name_cell:
                current_product = product_name_cell.strip()
                if str(type(current_payment)) == "<class 'float'>":
                    current_payment = str(current_payment*100) + "%"
                else:
                    current_payment = current_payment.strip()
                if str(type(current_period)) == "<class 'float'>":
                    current_period = str(current_period*100) + "%"
                else:
                    current_period = current_period.strip()
                datadict["program_id"] = 1003
                datadict["product_name"] = product_name
                datadict["product_id"] = int(time.time())+id_index
                id_index += 1
                datadict["data"][current_product] = []
            else:
                if not payment_cell and not period_cell and not type_cell and not product_name_cell or row_index == nrows-1:
                    self.total_data_list.append(datadict)
                    datadict = {}
                    datadict["data"] = {}
                    product_name = ""
                    continue
            if period_cell and period_cell != current_period:
                current_period = period_cell

            detail_list.append(current_period)
            detail_list.append(current_payment)
            for col_index in range(4, table.row_len(row_index)):
                current_cell_value = table.cell_value(row_index, col_index)
                if current_cell_value:
                    if str(type(current_cell_value)) == "<class 'float'>":
                            current_cell_value = str(current_cell_value*100) + "%"
                            detail_list.append(current_cell_value)
                    else:
                            detail_list.append(current_cell_value)
            datadict["data"][current_product].append(detail_list)
        return self.total_data_list

    def Login(self):
        Login_headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01", 
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
        Login_PayLoad = {"loginName": self.userName, "loginPwd": self.password}
        self.Yisheng_Session.post(url=self.login_api, headers = Login_headers, data = Login_PayLoad)
        print("Login successfully!")

    def run(self):
        self.Login()
        data_list = self.__Excel_Handler()
        for datadict in data_list:
            product_key = datadict["product_name"]
            data = datadict["data"]
            Request_Payloads = {"productSup": "All", "pageIndex": 1, "productSearch": product_key, "orderbyFlag": 1, "prase": 1, "commission":4}
            Products_Res = self.Yisheng_Session.post(url = self.product_menu_api, headers = self.Headers, data = Request_Payloads)
            Products_Res_Data = json.loads(Products_Res.text)
            if "ProductList" in Products_Res_Data:
                if Products_Res_Data["ProductList"]:
                    product_dict = Products_Res_Data["ProductList"][0]
                    product_dict["data"] = data
                    datadict["product_id"] = int(product_dict["productId"])
                    datadict["data"] = json.dumps(product_dict, ensure_ascii=False)
                else:
                    product_dict = {}
                    product_dict["data"] = data
                    datadict["data"] = json.dumps(product_dict, ensure_ascii=False)
            else:
                product_dict = {}
                product_dict["data"] = data
                datadict["data"] = json.dumps(product_dict, ensure_ascii=False)
            res = requests.post(url="http://106.12.160.222:8002/save_json_data/", data=json.dumps(datadict))
            result = json.loads(res.text)
            if(result["result"] == False):
                print(datadict["product_name"] + ": 保存失败")


if __name__ == "__main__":
    y = Yisheng(file_name="nov.xls", sheet_name="11月")
    y.run()
