from sqlalchemy.orm import sessionmaker
try:
    from CLD_Project.manageDB.manage import engine, Program, Baoyun18
except:
    from Api.manageDB.manage import engine, Program, Baoyun18

class mysqlFunc:

    def __init__(self):
        DBsessionmaker = sessionmaker(bind=engine)
        self.session = DBsessionmaker()

    def insertDataToProgram(self, DataDict:dict):
        # Add_Program = Program(program_id = DataDict["program_id"], program_name = DataDict["program_name"])
        # self.session.add(Add_Program)
        print(Add_Detail)

    def insertDataToBaiyun18(self, DataDict:dict):
        # Add_Detail = Program(program_id = DataDict["program_id"], product_id = DataDict["product_id"])
        # self.session.add(Add_Detail)
            print(DataDict)
            Add_Detail = Baoyun18(program_id = DataDict["program_id"], temp_id = int(DataDict["temp_id"]), product_id = int(DataDict["product_id"]),
                                product_name = DataDict["product_name"], payDesc = DataDict["payDesc"], insureDesc = DataDict["insureDesc"],
                                first_rate = DataDict["first_rate"], second_rate = DataDict["second_rate"])
            self.session.add(Add_Detail)
            self.session.commit()
            return True

    def __del__(self):
        # self.session.commit()
        self.session.close()