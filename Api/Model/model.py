from pydantic import BaseModel

class ProgramModel(BaseModel):
    program_id: int = None
    program_name: str
    
class Baoyun18Model(BaseModel):
    program_id: int
    temp_id: int
    product_id: int
    product_name: str
    payDesc: str
    insureDesc: str
    first_rate: float
    second_rate: float

class Qixin18Model(BaseModel):
    program_id: int
    product_id: int
    product_name: str
    plan_Id: int
    company_id: int
    company_name:str
    isDetails: bool
    yearPolicyText: str
    insureAgeText: str
    economyText:str
    feeRateList_1: float
    feeRateList_2: float