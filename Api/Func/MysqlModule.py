import pymysql
from dbutils.pooled_db import PooledDB

class MysqlModule:

    def __init__(self):
        # 2为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        pool = PooledDB(pymysql,2,host='127.0.0.1',user='root',db='CLD',port=3306,setsession=['SET AUTOCOMMIT = 0'])
        self.DBConnection = pool.connection()
        # self.DBConnection = pymysql.connect(
        #     host = "127.0.0.1",
        #     port = 3306,
        #     user = "root",
        #     # password = "root",
        #     db = "CLD",
        #     charset = "utf8mb4" 
        # )

    def SaveDataToBaoyun18(self, DataDict:dict):
        select_sql = "SELECT `temp_id`, `product_id` FROM `CLD_Baoyun18` WHERE `temp_id` = %s AND `product_id` = %s AND payDesc = %s AND insureDesc = %s;"
        insert_sql = "INSERT INTO `CLD_Baoyun18` (`program_id`, `temp_id`, `product_id`, `product_name`, `payDesc`, `insureDesc`, `first_rate`, `second_rate`)\
                      values (%s, %s, %s, %s, %s, %s, %s, %s);"
        update_sql = "UPDATE CLD_Baoyun18 SET product_name = %s, first_rate = %s, second_rate = %s \
                      WHERE temp_id = %s AND product_id = %s AND payDesc = %s AND insureDesc = %s;"
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql, (DataDict["temp_id"],DataDict["product_id"], DataDict["payDesc"],DataDict["insureDesc"]))
            select_result = cursor.fetchone()
            # 存在数据就更新，不存在就插入
            if select_result:
                cursor.execute(update_sql, (DataDict["product_name"], DataDict["first_rate"], DataDict["second_rate"], DataDict["temp_id"],
                                DataDict["product_id"], DataDict["payDesc"], DataDict["insureDesc"]
                            ))
            else:
                cursor.execute(insert_sql, (DataDict["program_id"], DataDict["temp_id"], DataDict["product_id"], DataDict["product_name"],
                                DataDict["payDesc"], DataDict["insureDesc"], DataDict["first_rate"],DataDict["second_rate"]
                            ))
        self.DBConnection.commit()
        return True
        
    def SaveDataToQixin18(self, DataDict:dict):
        select_sql = "SELECT `product_id`,`plan_Id` FROM `CLD_Qixin18` WHERE `product_id` = %s AND `plan_Id` = %s AND `yearPolicyText` = %s AND `insureAgeText` = %s AND `economyText` = %s;"
        insert_sql = "INSERT INTO `CLD_Qixin18` (`program_id`, `product_id`, `product_name`, `plan_Id`, `company_id`, `company_name`, `yearPolicyText`, `insureAgeText`, `economyText`, `feeRateList_1`, `feeRateList_2`)\
                      values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        update_sql = "UPDATE CLD_Qixin18 SET `product_name` = %s, `company_id` = %s, `company_name` = %s, `feeRateList_1` = %s, `feeRateList_2` = %s\
                     WHERE `product_id` = %s AND `plan_Id` = %s AND `yearPolicyText` = %s AND `insureAgeText` = %s AND economyText = %s;"
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql, (DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"],DataDict["insureAgeText"], DataDict["economyText"]))
            select_result = cursor.fetchone()
            if select_result:
                cursor.execute(update_sql, (DataDict["product_name"], DataDict["company_id"], DataDict["company_name"],
                                DataDict["feeRateList_1"], DataDict["feeRateList_2"], DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["economyText"]
                            ))
            else:
                cursor.execute(insert_sql, (DataDict["program_id"], DataDict["product_id"], DataDict["product_name"], DataDict["plan_Id"],
                                DataDict["company_id"], DataDict["company_name"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["economyText"], DataDict["feeRateList_1"], DataDict["feeRateList_2"]
                            ))
        self.DBConnection.commit()
        return True
    
    def SaveDataToNiubao100(self, DataDict:dict):
        delete_sql = "DELETE FROM CLD_Niubao100 WHERE `product_id` = {product_id};"
        insert_sql_of_type_1 = "INSERT INTO CLD_Niubao100 (`program_id`, `product_id`, `product_name`, `version`, `ratio`, `renew_ratio`, `Type`) VALUES \
                               ({program_id}, {product_id}, '{product_name}', '{version}', '{ratio}', '{renew_ratio}', {Type});"
        insert_sql_of_type_2 = "INSERT INTO CLD_Niubao100 (`program_id`, `product_id`, `product_name`, `insuranceType`, `paytime`, `savetime`, `actratio`,`y1`, `y2`, `y3`, `y4`, `y5`, `Type`) VALUES \
                                ({program_id}, {product_id}, '{product_name}', '{insuranceType}', '{paytime}', '{savetime}', {actratio}, {y1}, {y2}, {y3}, {y4}, {y5}, {Type});"
        try:
            Type = DataDict["Type"]               
            with self.DBConnection.cursor() as cursor:
                # cursor.execute(delete_sql.format(product_id = DataDict["product_id"]))
                if Type == 1:                   
                    cursor.execute(insert_sql_of_type_1.format(program_id=DataDict["program_id"],product_id=DataDict["product_id"], product_name=DataDict["product_name"],
                                                               version=DataDict["version"], ratio=DataDict["ratio"], renew_ratio=DataDict["renew_ratio"],
                                                               Type=Type))
                else:
                    cursor.execute(insert_sql_of_type_2.format(program_id=DataDict["program_id"],product_id=DataDict["product_id"], product_name=DataDict["product_name"],
                                                               insuranceType=DataDict["insuranceType"], paytime=DataDict["paytime"], savetime=DataDict["savetime"],
                                                               actratio=DataDict["actratio"], y1=DataDict["y1"], y2=DataDict["y2"], y3=DataDict["y3"], y4=DataDict["y4"], 
                                                               y5=DataDict["y5"], Type=Type))
            self.DBConnection.commit()
            return {"result": True, "reason": None}
        except Exception as e:
            self.DBConnection.rollback()
            return {"result": False, "reason": e}
    
    def SaveDataToZhongbao(self, DataDict:dict):
        insert_sql = "INSERT INTO CLD_Zhongbao ({DataKeyList}) VALUES ({DataValuesList});"
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
        real_insert_sql = insert_sql.format(DataKeyList=",".join(DataKeyList), DataValuesList=",".join(DataValueList))
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(real_insert_sql)
            self.DBConnection.commit()
            return {"result": True, "reason": None}
        except Exception as e:
            print("save zhongbao data failed, the reason is: {reason}".format(reason = e))
            return {"result": False, "reason": e}

    def SaveDataToFengqi(self, DataDict:dict):
        insert_sql = "INSERT INTO CLD_Fengqi ({DataKeyList}) VALUES ({DataValuesList});"
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
        real_insert_sql = insert_sql.format(DataKeyList=",".join(DataKeyList), DataValuesList=",".join(DataValueList))
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(real_insert_sql)
            self.DBConnection.commit()
            return {"result": True, "reason": None}
        except Exception as e:
            print("save zhongbao data failed, the reason is: {reason}".format(reason = e))
            return {"result": False, "reason": e}

    def GetDataFromBaoyun18(self, datadict:dict) -> dict:
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
            "total_num": 0,
            "isEnd": False
        }
        if(datadict["searchType"] == 1 and datadict["program_id"] == 1000):
            if(datadict["product_key"] is None):
                select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Baoyun18 ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(page=(datadict["page"]-1)*5)
            else:
                select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Baoyun18 WHERE `product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)
            select_sql = "SELECT `program_id`,`product_id`,`product_name`,`payDesc`,`insureDesc`,`first_rate`,`second_rate`\
                        FROM CLD_Baoyun18 WHERE `product_id` = %s"
            try:
                with self.DBConnection.cursor() as cursor:
                    cursor.execute(select_product_sql)
                    result_set = cursor.fetchall()
                if(len(result_set) < 0):
                    result["isEnd"] = True
                    return result
                for product_id in result_set:
                    with self.DBConnection.cursor() as cursor_2:
                        cursor_2.execute(select_sql, product_id)
                        result_set_2 = cursor_2.fetchall()
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
                                "主费率": item[5],
                                "附件费率": item[6]
                            }
                            result_dict["details"].append(detail_dict)
                        result["result_list"].append(result_dict)     
                with self.DBConnection.cursor() as cursor:        
                    if(datadict["product_key"] is None):
                        count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Baoyun18;"
                    else:
                        count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Baoyun18 WHERE `product_name` LIKE '%{product_key}%';".format(product_key = datadict["product_key"])
                    cursor.execute(count_sql)
                    count = cursor.fetchone()
                    print(count)
                    result["total_num"] = int(count[0])
                return result
            except Exception as e:
                result["success"] = False
                print("Failed to get data from baoyun18: ")
                print(e)
                result["fail_reason"] = e
                return result

    def GetDataFromNiubao100(self, datadict:dict) -> dict:
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
            "total_num": 0,
            "isEnd": False
        }
        if(datadict["product_key"] is None):
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM `CLD_Niubao100` ORDER BY `product_id` ASC LIMIT 5 OFFSET {page};".format(page=(datadict["page"]-1)*5)
        else:
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM `CLD_Niubao100` WHERE `product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT 5 OFFSET {page};".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)

        select_sql = "SELECT `program_id`,`product_id`,`product_name`, `insuranceType`,`paytime`,`savetime`,\
                    `actratio`, `y1`, `y2`, `y3`,`y4`, `y5`,`version`, `ratio`, `renew_ratio`, `Type` \
                    FROM `CLD_Niubao100` WHERE `product_id` = %s;"  

        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_product_sql)
                result_set = cursor.fetchall()
                if(len(result) < 0):
                    result["isEnd"] = True
                    return result
                for product_id in result_set:
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
                    result["result_list"].append(result_dict)                    
            with self.DBConnection.cursor() as cursor:        
                if(datadict["product_key"] is None):
                    count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Niubao100;"
                else:
                    count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Niubao100 WHERE `product_name` LIKE '%{product_key}%';".format(product_key = datadict["product_key"])
                cursor.execute(count_sql)
                count = cursor.fetchone()
                result["total_num"] = int(count[0])
            return result
        except Exception as e:
            result["success"] = False
            result["fail_reason"] = e
            print(e)
            return result

    def GetDataFromQixin18(self, datadict:dict) -> dict:
        result = {
                    "success": True,
                    "fail_reason": None,
                    "result_list": [],
                    "total_num": 0,
                    "isEnd": False
        }
        if(datadict["product_key"] is None):
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Qixin18 ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(page=(datadict["page"]-1)*5)
        else:
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Qixin18 WHERE `product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)

        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`yearPolicyText`,`insureAgeText`,\
                    `economyText`, `feeRateList_1`, `feeRateList_2` FROM CLD_Qixin18 WHERE `product_id` = %s;"  
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(select_product_sql)
                result_set = cursor.fetchall()
                if(len(result) < 0):
                    result["isEnd"] = True
                    return result
                for product_id in result_set:
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
                    result["result_list"].append(result_dict)                    
            with self.DBConnection.cursor() as cursor:        
                if(datadict["product_key"] is None):
                    count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Qixin18;"
                else:
                    count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Qixin18 WHERE `product_name` LIKE '%{product_key}%';".format(product_key = datadict["product_key"])
                cursor.execute(count_sql)
                count = cursor.fetchone()
                result["total_num"] = int(count[0])
            return result
        except Exception as e:
            result["success"] = False
            result["fail_reason"] = e
            print(e)
            return result

    def GetDataFromZhongbao(self, datadict) -> dict:
        result = {
                    "success": True,
                    "fail_reason": None,
                    "result_list": [],
                    "total_num": 0,
                    "isEnd": False
        }
        if datadict["product_key"]:
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Zhongbao ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(page=(datadict["page"]-1)*5)
        else:
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Zhongbao WHERE `product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)

        select_sql = "SELECT `program_id`,`product_id`,`product_name`,`clauseId`,`clauseName`,\
                    `extraType`, `rateCodeDescView`, `rateCode`, `rateCodeDesc`, `yearCode`, `yearCodeDesc`,\
                    `first_rate`, `second_rate`, `third_rate`, `fourth_rate`, `fifth_rate`FROM CLD_Zhongbao WHERE `product_id` = %s ORDER BY `extraType`;"       
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_product_sql)
            result_set = cursor.fetchall()
            if(len(result) < 0):
                result["isEnd"] = True
                return result
            for product_id in result_set:
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
                        rateCodeDescView_dict[rateCodeDescView_dict].append(rateCodeDescView_detail)
                    else:
                        rateCodeDescView_dict[rateCodeDescView] = []
                        rateCodeDescView_dict[rateCodeDescView].append(rateCodeDescView_detail)
                    details_dict["rateCodeDescViewList"] = rateCodeDescView_dict

                    if details_dict["clauseId"] in product_detail.keys():
                        product_detail[details_dict["clauseId"]].append(details_dict)
                    else:
                        product_detail[details_dict["clauseId"]] = []
                        product_detail[details_dict["clauseId"]].append(details_dict)
                result_dict["details"].append(product_detail)
            result["result_list"].append(result_dict)
        with self.DBConnection.cursor() as cursor:        
            if(datadict["product_key"] is None):
                count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Qixin18;"
            else:
                count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM CLD_Qixin18 WHERE `product_name` LIKE '%{product_key}%';".format(product_key = datadict["product_key"])
            cursor.execute(count_sql)
            count = cursor.fetchone()
            result["total_num"] = int(count[0]) 
        return result    
        # except Exception as e:
        #     result["success"] = False
        #     result["fail_reason"] = e
        #     print(e)
        #     return result


    def GetDataFromAll(self, datadict:dict) -> dict:
        # print("GetDataFromAll Start")
        result = {
                    "success": True,
                    "fail_reason": None,
                    "result_list": [],
                    "isEnd": False
        }        
        try:
            if datadict["product_key"]:
                select_sql_of_all = "SELECT `program_id`, `product_id`,`product_name` FROM \
                ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`)) AS e \
                WHERE e.`product_name` LIKE '%{product_key}%' ORDER BY `product_id` ASC LIMIT 5 OFFSET {page};"
                # print("GetDataFromAll have product_key")
                with self.DBConnection.cursor() as cursor:
                    # print("GetDataFromAll search product in all program")
                    cursor.execute(select_sql_of_all.format(product_key = datadict["product_key"], page=(datadict["page"]-1)*5))
                    result_set = cursor.fetchall()
                    # print("product in all program")
                    # print(result_set)
                    if(len(result_set) < 0):
                        result["isEnd"] = True
                        return result
                    for detail_result in result_set:
                        result_dict = {
                            "program_id": detail_result[0],
                            "product_id": detail_result[1],
                            "product_name": detail_result[2],
                            "details":[]
                        }
                        if(result_dict["program_id"] == 1000):
                            # baoyun100 add detail
                            # print("program_id == 1000")
                            select_sql_of_baoyun18 = "SELECT `program_id`,`product_id`,`product_name`,`payDesc`,`insureDesc`,`first_rate`,`second_rate`\
                            FROM CLD_Baoyun18 WHERE `product_id` = %s;"
                            cursor.execute(select_sql_of_baoyun18,(result_dict["product_id"],))
                            result_set_of_Baoyun18 = cursor.fetchall()
                            for item in result_set_of_Baoyun18:
                                detail_dict = {
                                    "缴费年限": item[3],#yearPolicyText
                                    "保障年限": item[4], #insureAgeText
                                    "主费率": item[5], #economyText
                                    "附加费率":item[6], #feeRateList_1
                                }
                                result_dict["details"].append(detail_dict)
                            # print("baoyun18: ")
                            # print(result_dict)
                            result["result_list"].append(result_dict)
                        elif(result_dict["program_id"] == 1001):
                            # qixin18 add detail
                            select_sql_of_qixin18 = "SELECT `program_id`,`product_id`,`product_name`,`yearPolicyText`,`insureAgeText`,\
                                                    `economyText`, `feeRateList_1`, `feeRateList_2` FROM CLD_Qixin18 WHERE `product_id` = %s;"
                            cursor.execute(select_sql_of_qixin18,(result_dict["product_id"],))
                            result_set_of_qixin18 = cursor.fetchall()
                            for item in result_set_of_qixin18:
                                detail_dict = {
                                    "保单年度": item[3],#yearPolicyText
                                    "缴费年限": item[4], #insureAgeText
                                    "缴费纬度": item[5], #economyText
                                    "主险":item[6], #feeRateList_1
                                    "附加险":item[7] #feeRateList_2
                                }
                                result_dict["details"].append(detail_dict)
                            # print("qixin18: ")
                            # print(result_dict)
                            result["result_list"].append(result_dict)
                        elif(result_dict["program_id"] == 1002):
                            select_sql_of_niubao100 = "SELECT `program_id`,`product_id`,`product_name`, `insuranceType`,`paytime`,`savetime`,\
                                                    `actratio`, `y1`, `y2`, `y3`,`y4`, `y5`,`version`, `ratio`, `renew_ratio`, `Type` \
                                                    FROM `CLD_Niubao100` WHERE `product_id` = %s;" 
                            cursor.execute(select_sql_of_niubao100,(result_dict["product_id"],))
                            result_set_of_niubao100 = cursor.fetchall()
                            for item in result_set_of_niubao100:
                                # 判断type
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
                            result["result_list"].append(result_dict)
                with self.DBConnection.cursor() as cursor:        
                    count_sql = "SELECT COUNT(DISTINCT(`product_id`)) AS COUNT FROM ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`)) AS e where e.`product_name` LIKE '%{product_key}%';".format(product_key = datadict["product_key"])
                    cursor.execute(count_sql)
                    count = cursor.fetchone()
                    result["total_num"] = int(count[0])
                return result
            else:
                # print("GetDataFromAll have not product_key")
                select_sql_of_all = "SELECT `program_id`, `product_id`,`product_name` FROM \
                ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`)) AS e \
                ORDER BY `product_id` ASC LIMIT 5 OFFSET %s;"
                with self.DBConnection.cursor() as cursor:
                    cursor.execute(select_sql_of_all, ((datadict["page"]-1)*5,))
                    result_set = cursor.fetchall()
                    if(len(result_set) < 0):
                        result["isEnd"] = True
                        return result
                    for detail_result in result_set:
                        result_dict = {
                            "program_id": detail_result[0],
                            "product_id": detail_result[1],
                            "product_name": detail_result[2],
                            "details":[]
                        }
                        if(result_dict["program_id"] == 1000):
                            # baoyun100 add detail
                            select_sql_of_baoyun18 = "SELECT `program_id`,`product_id`,`product_name`,`payDesc`,`insureDesc`,`first_rate`,`second_rate`\
                            FROM CLD_Baoyun18 WHERE `product_id` = %s;"
                            cursor.execute(select_sql_of_baoyun18,(result_dict["product_id"],))
                            result_set_of_Baoyun18 = cursor.fetchall()
                            for item in result_set_of_Baoyun18:
                                detail_dict = {
                                    "缴费年限": item[3],#yearPolicyText
                                    "保障年限": item[4], #insureAgeText
                                    "主费率": item[5], #economyText
                                    "附加费率":item[6], #feeRateList_1
                                }
                                result_dict["details"].append(detail_dict)
                            result["result_list"].append(result_dict)
                        elif(result_dict["program_id"] == 1001):
                            # qixin18 add detail
                            select_sql_of_qixin18 = "SELECT `program_id`,`product_id`,`product_name`,`yearPolicyText`,`insureAgeText`,\
                                                    `economyText`, `feeRateList_1`, `feeRateList_2` FROM CLD_Qixin18 WHERE `product_id` = %s;"
                            cursor.execute(select_sql_of_qixin18,(result_dict["product_id"],))
                            result_set_of_qixin18 = cursor.fetchall()
                            for item in result_set_of_qixin18:
                                detail_dict = {
                                    "保单年度": item[3],#yearPolicyText
                                    "缴费年限": item[4], #insureAgeText
                                    "缴费纬度": item[5], #economyText
                                    "主险":item[6], #feeRateList_1
                                    "附加险":item[7] #feeRateList_2
                                }
                                result_dict["details"].append(detail_dict)
                            result["result_list"].append(result_dict)
                        elif(result_dict["program_id"] == 1002):
                            select_sql_of_niubao100 = "SELECT `program_id`,`product_id`,`product_name`, `insuranceType`,`paytime`,`savetime`,\
                                                    `actratio`, `y1`, `y2`, `y3`,`y4`, `y5`,`version`, `ratio`, `renew_ratio`, `Type` \
                                                    FROM `CLD_Niubao100` WHERE `product_id` = %s;" 
                            cursor.execute(select_sql_of_niubao100,(result_dict["product_id"],))
                            result_set_of_niubao100 = cursor.fetchall()
                            for item in result_set_of_niubao100:
                                # 判断type
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
                            result["result_list"].append(result_dict)
                with self.DBConnection.cursor() as cursor:        
                    count_sql = "SELECT COUNT(DISTINCT(e.`product_id`)) AS COUNT FROM ((SELECT `program_id`,`product_id`, `product_name` FROM `CLD_Baoyun18`) union \
                                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Qixin18`) union \
                                (SELECT `program_id`, `product_id`, `product_name` FROM `CLD_Niubao100`)) AS e;"
                    cursor.execute(count_sql)
                    count = cursor.fetchone()
                    result["total_num"] = int(count[0])
                return result
        except Exception as e:
            result["success"] = False
            result["fail_reason"] = e
            print(e)
            return result

    def __del__(self):
        try:
            self.DBConnection.cursor().close()
        except Exception as e:
            print("close cursor failed: ")
            print(e)
        self.DBConnection.close()