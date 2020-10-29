import pymysql
from dbutils.pooled_db import PooledDB

class DBHandler:
    def __init__(self):

        # connect pool
        # 2为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        pool = PooledDB(pymysql, 2, host='127.0.0.1', user='root', db='CLD', port=3306, setsession=['SET AUTOCOMMIT = 0'])
        self.DBConnection = pool.connection()
    
    def SaveDataToDB(self, datadict:dict) -> bool:
        """
        @params: datadict, 字典类型, keys包括:
        program_id -> int: 平台id
        program_name -> str: 平台名称
        program_db_name -> str: db名称
        product_id -> bigint: 产品id
        product_name -> str: 产品名称
        detail_header -> str: 详细页表头
        detail_list -> list: 详细页行记录列表 
        """
        excute_sql_string = "START TRANSACTION;"
        for detail_dict in datadict["detail_list"]:
            column_name_str, values_list_str = self.changeDataDictToStr(detail_dict)
            save_sql_string = "INSERT INTO `{db_name}` ({column_names}) VALUES ({values_list});".format(
                dbname = datadict["program_db_name"],
                column_names = column_name_str,
                values_list = values_list_str
            )
            excute_sql_string += save_sql_string
        excute_sql_string += "COMMIT;"
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(excute_sql_string)
            self.DBConnection.commit()
            return True
        except Exception as e:
            print("Save Data To {db_name} Fail.\nThe reason is: {reason}".format(
                db_name=datadict["program_db_name"],
                reason = e
            ))
            self.DBConnection.rollback()
            return False
            
    def GetDataFromDB(self, datadict:dict) -> dict:
        """
        @params: datadict, 字典类型, keys包含:
        searchType -> int: 全部为1
        program_id -> int: 平台id, 用于判断平台
        product_key -> str: 产品关键字, 用于搜索产品
        page -> int: 页数
        pageSize -> int: 每页显示数量
        """
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
            "total_num": 0,
        }
        program_id = datadict["program_id"]
        if program_id == 1000:
            db_name = "CLD_Baoyun18"
        elif program_id == 1001:
            db_name = "CLD_Qixin18"
        elif program_id == 1002:
            db_name = "CLD_Niubao100"
        elif program_id == 1003:
            db_name = "CLD_Fengqi"
        elif program_id == 1004:
            db_name = "CLD_Zhongbao"
        else:
            # all
            result = self.__GetDataFromAll(datadict)
            return result
        if datadict["product_key"]:
            select_product_id_sql_string = "SELECT DISTINCT(`product_id`) FROM {db_name} \
                WHERE `product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC \
                LIMIT {pageSize} OFFSET {page};".format(
                    db_name = db_name,
                    product_key = datadict["product_key"],
                    pageSize=datadict["pageSize"],
                    page = (datadict["page"]-1)*datadict["pageSize"])
            count_sql = "SELECT COUNT(DISTINCT(`product_id`)) FROM {db_name} \
                WHERE `product_name` LIKE '%{product_key}%'".format(
                    db_name = db_name,
                    product_key = datadict["product_key"],
                )
        else:
            select_product_id_sql_string = "SELECT DISTINCT(`product_id`) FROM {db_name} \
                ORDER BY `product_id` ASC LIMIT {pageSize} OFFSET {page};".format(
                    db_name = db_name,
                    product_key = datadict["product_key"],
                    pageSize=datadict["pageSize"],
                    page = (datadict["page"]-1)*datadict["pageSize"])
            count_sql = "SELECT COUNT(DISTINCT(`product_id`)) FROM {db_name}".format(
                    db_name = db_name
                )
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_product_id_sql_string)
            result_set = cursor.fetchall()

            # total_num
            cursor.execute(count_sql)
            total_num = cursor.fetchall()
            print(total_num)
            result["total_num"] = total_num[0][0]
        if result["total_num"] <= 0:
            return result
        for product_id in result_set:
            if program_id == 1000:
                # Baoyun18
                result_dict = self.__GetDataFromBaoyun18(product_id)
            elif program_id == 1001:
                # Qixin18
                result_dict = self.__GetDataFromQixin18(product_id)
            elif program_id == 1002:
                # Niubao100
                result_dict = self.__GetDataFromNiubao100(product_id)
            elif program_id == 1004:
                # Fengqi
                result_dict = self.__GetDataFromFengqi(product_id)
            elif program_id == 1005:
                result_dict = self.__GetDataFromZhongbao(product_id)
            else:
                result_dict = []
            result["result_list"].append(result_dict)
        return result
    
    def __GetDataFromBaoyun18(self, product_id) -> dict:
        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`payDesc`,`insureDesc`,`first_rate`,`second_rate`\
                      FROM CLD_Baoyun18 WHERE `product_id` = %s;"
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql, product_id)
            result_set_2 = cursor.fetchall()
            result_dict = {
                "program_id": result_set_2[0][0],
                "product_id": result_set_2[0][1],
                "product_name": result_set_2[0][2],
                "details":[]
            }
            for item in result_set_2:
                detail_dict = {
                    "缴费年限": item[3],
                    "保障年限": item[4],
                    "首年": item[5],
                    "次年": item[6]
                }
                result_dict["details"].append(detail_dict)
        return result_dict

    def __GetDataFromQixin18(self, product_id) -> dict:
        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`yearPolicyText`,`insureAgeText`,\
                    `economyText`, `feeRateList_1`, `feeRateList_2` FROM CLD_Qixin18 WHERE `product_id` = %s;"
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_sql, product_id)
                result_set = cursor.fetchall()
                result_dict = {
                    "program_id": result_set[0][0],
                    "product_id": result_set[0][1],
                    "product_name": result_set[0][2],
                    "details":[]
                }
                for item in result_set:
                    detail_dict = {
                        "保单年度": item[3],#yearPolicyText
                        "缴费年限": item[4], #insureAgeText
                        "缴费纬度": item[5], #economyText
                        "主险":item[6], #feeRateList_1
                        "附加险":item[7] #feeRateList_2
                    }
                    result_dict["details"].append(detail_dict)
            return result_dict
        except Exception as e:
            print("Get Data From Qixin....\n")
            print(str(e)+"\n")
            result_dict = {
                "program_id": -1,
                "product_id": -1,
                "product_name": "",
                "details":[]
            }
            return result_dict

    def __GetDataFromNiubao100(self, product_id) -> dict:
        select_sql = "SELECT `program_id`,`product_id`,`product_name`, `insuranceType`,`paytime`,`savetime`,\
                    `actratio`, `y1`, `y2`, `y3`,`y4`, `y5`,`version`, `ratio`, `renew_ratio`, `Type` \
                    FROM `CLD_Niubao100` WHERE `product_id` = %s;"
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_sql, product_id)
                result_set = cursor.fetchall()
                result_dict = {
                    "program_id": result_set[0][0],
                    "product_id": result_set[0][1],
                    "product_name": result_set[0][2],
                    "details":[]
                }
                for item in result_set:
                    if item[15] == 1:
                        detail_dict = {
                            "版本号": item[12],
                            "基础费率":item[13],
                            "续保费率":item[14]
                        }
                    else:    
                        detail_dict = {
                            "险种产品名称": item[3],
                            "缴费年限": item[4],
                            "保障年限": item[5],# savetime
                            "活动补贴":item[6],
                            "首年推广费比例":item[7],
                            "第二年推广费比例": item[8],
                            "第三年推广费比例": item[9],
                            "第四年推广费比例": item[10],
                            "第五年推广费比例": item[11]
                        }
                    result_dict["details"].append(detail_dict)
            return result_dict
        except Exception as e:
            print("Get Data From Niubao100....\n")
            print(str(e)+"\n")
            result_dict = {
                "program_id": -1,
                "product_id": -1,
                "product_name": "",
                "details":[]
            }
            return result_dict

    def __GetDataFromFengqi(self, product_id) -> dict:
        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`productGrade`,`productGradeId`,\
                    `curBack`, `commission_1`, `subsidyCommission_1`,`commission_2`, `subsidyCommission_2`,\
                    `commission_3`, `subsidyCommission_3`, `commission_4`, `subsidyCommission_4`, \
                    `commission_5`, `subsidyCommission_5`,`commission_6`, `subsidyCommission_6` \
                    FROM CLD_Fengqi WHERE `product_id` = %s;"  
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_sql, product_id)
                result_set = cursor.fetchall()
                result_dict = {
                    "program_id": result_set[0][0],
                    "product_id": result_set[0][1],
                    "product_name": result_set[0][2],
                    "details":[]
                }
                productGrade_dict = {}
                    # productGrade_dict里面包含该产品下的所有表
                    # {"123":{"c1":1,"c2":2},.....}              
                for record_set in result_set:
                    productGradeDetail_dict = {}
                    productGradeId = record_set[4]
                    productGradeDetail_dict["productGrade"] = record_set[3]
                    productGradeDetail_dict["commission_1"] = record_set[6]
                    productGradeDetail_dict["subsidyCommission_1"] = record_set[7]
                    productGradeDetail_dict["commission_2"] = record_set[8]
                    productGradeDetail_dict["subsidyCommission_2"] = record_set[9]
                    productGradeDetail_dict["commission_3"] = record_set[10]
                    productGradeDetail_dict["subsidyCommission_3"] = record_set[11]
                    productGradeDetail_dict["commission_4"] = record_set[12]
                    productGradeDetail_dict["subsidyCommission_4"] = record_set[13]
                    productGradeDetail_dict["commission_5"] = record_set[14]
                    productGradeDetail_dict["subsidyCommission_5"] = record_set[15]
                    productGradeDetail_dict["commission_6"] = record_set[16]
                    productGradeDetail_dict["subsidyCommission_6"] = record_set[17]
                    if productGradeId in productGrade_dict.keys():
                        productGrade_dict[productGradeId].append(productGradeDetail_dict)
                    else:
                        productGrade_dict[productGradeId] = []
                        productGrade_dict[productGradeId].append(productGradeDetail_dict)
                result_dict["details"].append(productGrade_dict)
            return result_dict
        except Exception as e:
            print("Get Data From Fengqi....\n")
            print(str(e)+"\n")
            result_dict = {
                "program_id": -1,
                "product_id": -1,
                "product_name": "",
                "details":[]
            }
            return result_dict

    def __GetDataFromZhongbao(self, product_id) -> dict:
        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`clauseId`,`clauseName`,\
                    `extraType`, `rateCodeDescView`, `rateCode`, `rateCodeDesc`, `yearCode`, `yearCodeDesc`,\
                    `first_rate`, `second_rate`, `third_rate`, `fourth_rate`, `fifth_rate`FROM CLD_Zhongbao \
                    WHERE `product_id` = %s ORDER BY `extraType`;" 
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_sql, product_id)
                result_set = cursor.fetchall()
                result_dict = {
                            "program_id": result_set[0][0],
                            "product_id": result_set[0][1],
                            "product_name": result_set[0][2],
                            "details":[]
                            # details里面保存数据结构：[{"1234":[{"clauseID": "12333"....,}, ],"5678":[{"clauseID": "12333"....,}, ] }]
                }
            # product_detail里面包含每个产品的每个表
                product_detail = {}
                # {"1234":[{"clauseID": "12333"....,} ,"5678":[{"clauseID": "12333"....,]}
                for record_set in result_set:
                    rateCodeDescView_dict = {}
                    details_dict = {}
                    rateCodeDescView_detail = {}
                    details_dict["clauseId"] = record_set[3]
                    details_dict["clauseName"] = record_set[4]
                    details_dict["extraType"] = record_set[5]
                    rateCodeDescView = record_set[6]
                    rateCodeDescView_detail["rateCodeDescView"] = rateCodeDescView
                    rateCodeDescView_detail["rateCode"] = record_set[7]
                    rateCodeDescView_detail["rateCodeDesc"] = record_set[8]
                    rateCodeDescView_detail["yearCode"] = record_set[9]
                    rateCodeDescView_detail["yearCodeDesc"] = record_set[10]
                    rateCodeDescView_detail["first_rate"] = record_set[11]
                    rateCodeDescView_detail["second_rate"] = record_set[12]
                    rateCodeDescView_detail["third_rate"] = record_set[13]
                    rateCodeDescView_detail["fourth_rate"] = record_set[14]
                    rateCodeDescView_detail["fifth_rate"] = record_set[15]
                    if rateCodeDescView in rateCodeDescView_dict.keys():
                        rateCodeDescView_dict[rateCodeDescView_detail["rateCode"]].append(rateCodeDescView_detail)
                    else:
                        rateCodeDescView_dict[rateCodeDescView_detail["rateCode"]] = []
                        rateCodeDescView_dict[rateCodeDescView_detail["rateCode"]].append(rateCodeDescView_detail)
                    details_dict["rateCodeDescViewList"] = rateCodeDescView_dict

                    if details_dict["clauseId"] in product_detail.keys():
                        product_detail[details_dict["clauseId"]].append(details_dict)
                    else:
                        product_detail[details_dict["clauseId"]] = []
                        product_detail[details_dict["clauseId"]].append(details_dict)
                result_dict["details"].append(product_detail)
            return result_dict
        except Exception as e:
            print("Get Data From Zhongbao....\n")
            print(str(e)+"\n")
            result_dict = {
                "program_id": -1,
                "product_id": -1,
                "product_name": "",
                "details":[]
            }
            return result_dict

    def __GetDataFromAll(self, datadict:dict) -> dict:
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
            "total_num": 0,
        }
        if datadict["product_key"]:
            select_sql_of_all = "SELECT `program_id`, `product_id`,`product_name` FROM \
            ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Zhongbao`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Fengqi`)) AS e \
            WHERE e.`product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT {pageSize} \
            OFFSET {page};".format(
                product_key = datadict["product_key"],
                pageSize = datadict["pageSize"],
                page = (datadict["page"]-1)*datadict["pageSize"]
            )
            count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Zhongbao`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Fengqi`)) AS e where e.`product_name` LIKE '%{product_key}%';".format(
                            product_key = datadict["product_key"])
        else:
            # GetDataFromAll have not product_key
            select_sql_of_all = "SELECT `program_id`, `product_id`,`product_name` FROM \
            ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Zhongbao`) union \
            (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Fengqi`)) AS e \
            ORDER BY `product_id` ASC LIMIT {pageSize} OFFSET {page};".format(
                pageSize = datadict["pageSize"],
                page = (datadict["page"]-1)*datadict["pageSize"]
            )
            count_sql = "SELECT COUNT(DISTINCT(e.`product_id`)) AS COUNT FROM ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Zhongbao`) union \
                        (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Fengqi`)) AS e;"
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_sql_of_all)
                result_set = cursor.fetchall()
                cursor.execute(count_sql)
                total_num = cursor.fetchall()
            result["total_num"] = total_num
            if result["total_num"] <=0 :
                return result
            for detail_result in result_set:
                result_dict = {
                    "program_id": detail_result[0],
                    "product_id": detail_result[1],
                    "product_name": detail_result[2],
                    "details":[]
                }
                if result_dict["program_id"] == 1000:
                    baoyun18_result_dict = self.__GetDataFromBaoyun18(product_id=result_dict["product_id"])
                    result["result_list"].append(baoyun18_result_dict)
                elif result_dict["program_id"] == 1001:
                    Qixin18_result_dict = self.__GetDataFromQixin18(product_id=result_dict["product_id"])
                    result["result_list"].append(Qixin18_result_dict)
                elif result_dict["program_id"] == 1002:
                    Niubao100_result_dict = self.__GetDataFromNiubao100(product_id=result_dict["product_id"])
                    result["result_list"].append(Niubao100_result_dict)
                elif result_dict["program_id"] == 1004:
                    Fengqi_result_dict = self.__GetDataFromFengqi(product_id=result_dict["product_id"])
                    result["result_list"].append(Fengqi_result_dict)
                elif result_dict["program_id"] == 1005:
                    Zhongbao_result_dict = self.__GetDataFromZhongbao(product_id=result_dict["product_id"])
                    result["result_list"].append(Zhongbao_result_dict)
                else:
                    baoyun18_result_dict = self.__GetDataFromBaoyun18(product_id=result_dict["product_id"])
                    result["result_list"].append(baoyun18_result_dict)
            return result
        except Exception as e:
            print("Get ALL...\n")
            print(str(e)+"\n")
            result = {
                "success": False,
                "fail_reason": e,
                "result_list": [],
                "total_num": 0,
            }
            return result

    @staticmethod
    def changeDataDictToStr(DataDict:dict) -> str:
        DataKeyList = []
        DataValueList = []
        for key, value in DataDict.items():
                keyStr = "`" + key + "`"
                if(type(value) == str):
                   valueStr = "'" + value + "'"
                else:
                   valueStr = str(value)
                DataKeyList.append(keyStr)
                DataValueList.append(valueStr)
        key_result_str = ",".join(DataKeyList)
        value_result_str = ",".join(DataValueList)
        return key_result_str, value_result_str

    def __del__(self):
        print("DBHandler Close....")
        self.DBConnection.close()