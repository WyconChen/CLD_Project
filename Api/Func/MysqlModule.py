import pymysql


class MysqlModule:

    def __init__(self):
        pass
        self.DBConnection = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            password = "chenweicong11",
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
    
    def GetDataFromBaoyun18(self):
        select_sql = "SELECT * FROM `CLD_Baoyun18` LIMIT 1;"
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql)
            select_result = cursor.fetchone()
        # self.DBConnection.commit()
        return select_result
    
    def SaveDataToQixin18(self, DataDict:dict):
        select_sql = "SELECT `product_id`,`plan_Id` WHERE `product_id` = %s AND `plan_Id` = %s AND `yearPolicyText` = %s AND `insureAgeText` = %s AND `enconmyText` = %s;"
        insert_sql = "INSERT INTO `CLD_Qixin18` (`program_id`, `product_id`, `product_name`, `plan_Id`, `company_id`, `company_name`, `isDetails`, `yearPolicyText`, `insureAgeText`, `enconomyText`, `feeRateList_1`, `feeRateList_2`)\
                      values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        update_sql = "UPDATE CLD_Qixin18 SET `product_name` = %s, `company_id` = %s, `company_name` = %s, `isDetails` = %s, `feeRateList_1` = %s, `feeRateList_2` = %s\
                     WHERE `product_id` = %s AND `plan_Id` = %s AND `yearPolicyText` = %s AND `insureAgeText` = %s AND enconmyText = %s;"
        print("DataDict is: "+ str(DataDict))
        with self.DBConnection.cursor() as cursor:
            cursor.execute(select_sql, (DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"],DataDict["insureAgeText"], DataDict["economyText"]))
            select_result = cursor.fetchone()
            if select_result:
                cursor.execute(update_sql, (DataDict["product_name"], DataDict["company_id"], DataDict["company_name"], DataDict["isDetails"],
                                DataDict["feeRateList_1"], DataDict["feeRateList_2"], DataDict["product_id"], DataDict["plan_Id"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["enconmyText"]
                            ))
            else:
                cursor.execute(insert_sql, (DataDict["program_id"], DataDict["product_id"], DataDict["product_name"], DataDict["plan_Id"],
                                DataDict["company_id"], DataDict["company_id"], DataDict["company_name"], DataDict["isDetails"], DataDict["yearPolicyText"], 
                                DataDict["insureAgeText"], DataDict["economyText"], DataDict["feeRateList_1"], DataDict["feeRateList_2"]
                            ))
        self.DBConnection.commit()
        return True

    def __del__(self):
        self.DBConnection.close()