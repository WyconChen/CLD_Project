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

class Niubao100Model(BaseModel):
    program_id: int
    item_id: int
    item_name: str
    sku_str: str
    sku: float
    insuranceType: str
    paytime: str
    savetime: str
    insuredage: str
    actratio: str
    y1: float
    y2: float
    y3: float
    y4: float
    y5: float

class Baoyun18DataModel(BaseModel):
    program_id: int
    page: int
    product_keyword: str