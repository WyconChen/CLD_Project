import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float

engine = create_engine("mysql+pymysql://root:chenweicong11@127.0.0.1:3306/CLD?charset=utf8mb4")

Base = declarative_base()

class Program(Base):
    __tablename__ = "CLD_Program"
    id = Column(Integer, primary_key = True)
    program_id = Column(Integer)
    program_name = Column(String(250))

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



if __name__ == "__main__":
    Base.metadata.create_all(engine)
