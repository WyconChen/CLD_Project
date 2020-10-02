import pymysql


class MysqlModule:

    def __init__(self):
        pass
        self.DBConnection = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            # password = "root",
            db = "CLD",
            charset = "utf8mb4" 
        )

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
        insert_sql = "INSERT INTO `CLD_Qixin18` (`program_id`, `product_id`, `product_name`, `plan_Id`, `company_id`, `company_name`, `isDetails`, `yearPolicyText`, `insureAgeText`, `economyText`, `feeRateList_1`, `feeRateList_2`)\
                      values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        update_sql = "UPDATE CLD_Qixin18 SET `product_name` = %s, `company_id` = %s, `company_name` = %s, `isDetails` = %s, `feeRateList_1` = %s, `feeRateList_2` = %s\
                     WHERE `product_id` = %s AND `plan_Id` = %s AND `yearPolicyText` = %s AND `insureAgeText` = %s AND economyText = %s;"
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql, (DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"],DataDict["insureAgeText"], DataDict["economyText"]))
            select_result = cursor.fetchone()
            if select_result:
                cursor.execute(update_sql, (DataDict["product_name"], DataDict["company_id"], DataDict["company_name"], DataDict["isDetails"],
                                DataDict["feeRateList_1"], DataDict["feeRateList_2"], DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["economyText"]
                            ))
            else:
                cursor.execute(insert_sql, (DataDict["program_id"], DataDict["product_id"], DataDict["product_name"], DataDict["plan_Id"],
                                DataDict["company_id"], DataDict["company_name"], DataDict["isDetails"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["economyText"], DataDict["feeRateList_1"], DataDict["feeRateList_2"]
                            ))
        self.DBConnection.commit()
        return True
    
    def SaveDataToNiubao100(self, DataDict:dict):
        delete_sql = "DELETE FROM CLD_Niubao100 WHERE `item_id` = %s;"
        insert_sql = "INSERT INTO CLD_Niubao100 (`program_id`, `item_id`, `item_name`, `sku_str`, `sku`, `insuranceType`, `paytime`, `savetime`, `insuredage`, `actratio`, \
            `y1`, `y2`, `y3`, `y4`, `y5`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            with self.DBConnection.cursor() as cursor:
                cursor.execute(delete_sql, (DataDict["item_id"],))
                cursor.execute(insert_sql, (DataDict["program_id"], DataDict["item_id"], DataDict["item_name"], DataDict["sku_str"], DataDict["sku"],
                            DataDict["insuranceType"], DataDict["paytime"], DataDict["savetime"], DataDict["insuredage"], DataDict["actratio"], 
                            DataDict["y1"], DataDict["y2"], DataDict["y3"], DataDict["y4"], DataDict["y5"]))
            self.DBConnection.commit()
            return {"result": True, "reason": None}
        except Exception as e:
            self.DBConnection.rollback()
            return {"result": False, "reason": e}
    
    def GetDataFromBaoyun18(self, datadict:dict) -> dict:
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
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
                                "pyDesc": item[3],
                                "insureDesc": item[4],
                                "first_rate": item[5],
                                "second_rate": item[6]
                            }
                            result_dict["details"].append(detail_dict)
                        result["result_list"].append(result_dict)                    
                return result
            except Exception as e:
                result["success"] = False
                result["fail_reason"] = e
                return result

    def GetDataFromNiubao100(self, datadict:dict) -> dict:
        result = {
            "success": True,
            "fail_reason": None,
            "result_list": [],
            "isEnd": False
        }
        if(datadict["product_key"] is None):
            select_product_sql = "SELECT DISTINCT(`item_id`) FROM CLD_Niubao100 ORDER BY `item_id` ASC LIMIT 5 OFFSET {page}".format(page=(datadict["page"]-1)*5)
        else:
            select_product_sql = "SELECT DISTINCT(`item_id`) FROM CLD_Niubao100 WHERE `item_name` LIKE '%{product_key}%' ORDER BY `item_id` ASC LIMIT 5 OFFSET {page}".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)

        select_sql = "SELECT `program_id`,`item_id`,`item_name`, `insuranceType`,`paytime`,`savetime`,\
                    `insuredage`, `actratio`, `y1`, `y2`, `y3`,`y4`, `y5`FROM CLD_Niubao100 WHERE `product_id` = %s;"  

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
                            "险种产品名称": item[3],
                            "缴费年限": item[4],
                            "savetime": item[5],# savetime
                            "insuredage": item[6], #insuredage
                            "活动补贴":item[7],
                            "首年推广费比例":item[8],
                            "第二年推广费比例": item[9],
                            "第三年推广费比例": item[10],
                            "第四年推广费比例": item[11],
                            "第五年推广费比例": item[12]
                        }
                        result_dict["details"].append(detail_dict)
                    result["result_list"].append(result_dict)                    
            return result
        except Exception as e:
            result["success"] = False
            result["fail_reason"] = e
            return result

    def GetDataFromQixin18(self, datadict:dict) -> dict:
        result = {
                    "success": True,
                    "fail_reason": None,
                    "result_list": [],
                    "isEnd": False
        }
        if(datadict["product_key"] is None):
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Qixin18 ORDER BY `product_id` ASC LIMIT 5 OFFSET {page}".format(page=(datadict["page"]-1)*5)
        else:
            select_product_sql = "SELECT DISTINCT(`product_id`) FROM CLD_Qixin18 WHERE `product_name` LIKE '%{product_key}%' ORDER BY `item_id` ASC LIMIT 5 OFFSET {page}".format(product_key = datadict["product_key"], page = (datadict["page"]-1)*5)

        select_sql = "SELECT `program_id`,`product_id`,`product_name`, `isDetails`,`yearPolicyText`,`insureAgeText`,\
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
                        "isDetail": result_set[0][3],
                        "details":[]
                    }
                    for item in result_set:
                        detail_dict = {
                            "保单年度": item[4],#yearPolicyText
                            "缴费年限": item[5], #insureAgeText
                            "缴费纬度": item[6], #economyText
                            "主险":item[7], #feeRateList_1
                            "附加险":item[8] #feeRateList_2
                        }
                        result_dict["details"].append(detail_dict)
                    result["result_list"].append(result_dict)                    
            return result
        except Exception as e:
            result["success"] = False
            result["fail_reason"] = e
            return result

    def __del__(self):
        self.DBConnection.close()