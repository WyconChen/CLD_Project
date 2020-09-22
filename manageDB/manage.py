import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float

engine = create_engine("mysql+pymysql://root:chenweicong11@127.0.0.1:3306/CLD?charset=utf8mb4")

Base = declarative_base()

class Program(Base):
    __tablename__ = "CLD_Program"
    id = Column(Integer, primary_key = True, auto_increment = True)
    program_id = Column(Integer)
    program_name = Column(String(250))

class Baoyun18(Base):
    __tablename__ = "CLD_Baoyun18"
    id = Column(Integer, primary_key = True, auto_increment = True)
    program_id = Column(Integer)
    temp_id = Column(Integer, nullable = False)
    product_id = Column(Integer, nullable = False)
    product_name = Column(String(250), nullable = False)
    payDesc = Column(String(250), nullable = False)
    insureDesc = Column(String(250),nullable = False, default = 0)
    first_rate = Column(Float, nullable = True)
    second_rate = Column(Float, nullable = True)



if __name__ == "__main__":
    Base.metadata.create_all(engine)
