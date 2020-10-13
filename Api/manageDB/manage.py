import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, Boolean

engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/CLD?charset=utf8mb4")

Base = declarative_base()

class Program(Base):
    __tablename__ = "CLD_Program"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    program_name = Column(String(250))
    product_id = Column(Integer)

    def __init__(self, program_id, program_name):
        self.program_id = program_id
        self.program_name = program_name

class Baoyun18(Base):
    __tablename__ = "CLD_Baoyun18"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    temp_id = Column(Integer, nullable = False)
    product_id = Column(Integer, nullable = False)
    product_name = Column(String(250), nullable = False)
    payDesc = Column(String(250), nullable = False)
    insureDesc = Column(String(250),nullable = False)
    first_rate = Column(Float, nullable = True)
    second_rate = Column(Float, nullable = True)
    
    def __init__(self, program_id, temp_id, product_id, product_name, payDesc, insureDesc, first_rate, second_rate):
        self.program_id = program_id
        self.temp_id = temp_id
        self.product_id = product_id
        self.product_name = product_name
        self.payDesc = payDesc
        self.insureDesc = insureDesc
        self.first_rate = first_rate
        self.second_rate = second_rate


class Qixin18(Base):
    __tablename__ = "CLD_Qixin18"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    product_id = Column(Integer, nullable = False)
    product_name = Column(String(250), nullable = False)
    plan_Id = Column(Integer, nullable = False)
    company_id = Column(Integer, nullable = False)
    company_name = Column(String(250), nullable = False)
    yearPolicyText = Column(String(250), nullable = True)
    insureAgeText = Column(String(250), nullable = True)
    economyText = Column(String(250), nullable = True)
    feeRateList_1 = Column(Float, nullable = True)
    feeRateList_2 = Column(Float, nullable = True)

class Niubao100(Base):
    __tablename__ = "CLD_Niubao100"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String(100), nullable = False)
    Type = Column(Integer)
    insuranceType = Column(String(100), nullable = True)
    paytime = Column(String(100), nullable = True)
    savetime = Column(String(100), nullable = True)
    actratio = Column(Float, nullable = True)
    y1 = Column(Float, nullable = True)
    y2 = Column(Float, nullable = True)
    y3 = Column(Float, nullable = True)
    y4 = Column(Float, nullable = True)
    y5 = Column(Float, nullable = True)
    version = Column(String(100),nullable = True)
    ratio = Column(String(100),nullable = True)
    renew_ratio = Column(String(100),nullable = True)

class Zhongbao(Base):
    __tablename__ = "CLD_Zhongbao"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String(100), nullable = False)
    clauseId = Column(String(100), nullable = False)
    clauseName = Column(String(100), nullable = False)
    extraType = Column(Integer)
    rateCodeDescView = Column(String(100), nullable = False)
    rateCode = Column(String(100), nullable = False)
    rateCodeDesc = Column(String(100), nullable = False)
    yearCode = Column(String(100))
    yearCodeDesc = Column(String(100))
    first_rate = Column(Float, nullable = True)
    second_rate = Column(Float, nullable = True)
    third_rate = Column(Float, nullable = True)
    fourth_rate = Column(Float, nullable = True)
    fifth_rate = Column(Float, nullable = True)

class Fengqi(Base):
    __tablename__ = "CLD_Fengqi"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String(100), nullable = False)
    productGrade = Column(String(100))
    productGradeId = Column(String(100))
    curBack = Column(Integer)
    commission_1 = Column(String(100))
    detail_id_1 = Column(String(100))
    payTerm_1 = Column(String(100))
    subsidyCommission_1 = Column(String(100))
    commission_2 = Column(String(100))
    detail_id_2 = Column(String(100))
    payTerm_2 = Column(String(100))
    subsidyCommission_2 = Column(String(100))
    commission_3 = Column(String(100))
    detail_id_3 = Column(String(100))
    payTerm_3 = Column(String(100))
    subsidyCommission_3 = Column(String(100))
    commission_4 = Column(String(100))
    detail_id_4 = Column(String(100))
    payTerm_4 = Column(String(100))
    subsidyCommission_4 = Column(String(100))
    commission_5 = Column(String(100))
    detail_id_5 = Column(String(100))
    payTerm_5 = Column(String(100))
    subsidyCommission_5 = Column(String(100))
    commission_6 = Column(String(100))
    detail_id_6 = Column(String(100))
    payTerm_6 = Column(String(100))
    subsidyCommission_6 = Column(String(100))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
