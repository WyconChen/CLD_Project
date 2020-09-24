from sqlalchemy.orm import sessionmaker
from manageDB.manage import engine, Program, Baoyun18

class mysqlFunc:

    def __init__(self):
        DBsessionmaker = sessionmaker(bind=engine)
        self.session = DBsessionmaker()

    def insertDataToProgram(self, DataDict:dict):
        Add_Program = Program(program_id = DataDict["program_id"], program_name = DataDict["program_name"])
        self.session.add(Add_Program)

    def insertDataToBaiyun18(self, DataDict:dict):
        Add_Detail = Program(program_id = DataDict["program_id"], product_id = DataDict["product_id"])
        self.session.add(Add_Detail)


    def __del__(self):
        self.session.commit()