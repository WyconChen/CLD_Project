import json
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
    yearPolicyText: str
    insureAgeText: str
    economyText:str
    feeRateList_1: float
    feeRateList_2: float

class Niubao100Model(BaseModel):
    program_id: int
    product_id: int
    product_name: str
    insuranceType: str
    paytime: str
    savetime: str
    actratio: str
    y1: float
    y2: float
    y3: float
    y4: float
    y5: float
    version: str
    ratio: str
    renew_ratio: str
    Type: int

class ZhongbaoModel(BaseModel):
    program_id: int
    product_id: int
    product_name: str
    clauseId: str
    clauseName: str
    extraType: int
    rateCodeDescView: str
    rateCode: str
    rateCodeDesc: str
    yearCode: str
    yearCodeDesc: str
    first_rate: float
    second_rate: float
    third_rate: float
    fourth_rate: float
    fifth_rate: float

class FengqiModel(BaseModel):
    program_id: int
    product_id: int
    product_name: str
    productGrade: str
    productGradeId: str
    curBack: int
    commission_1: str
    detail_id_1: str
    payTerm_1: str
    subsidyCommission_1: str
    commission_2: str
    detail_id_2: str
    payTerm_2: str
    subsidyCommission_2: str
    commission_3: str
    detail_id_3: str
    payTerm_3: str
    subsidyCommission_3: str
    commission_4: str
    detail_id_4: str
    payTerm_4: str
    subsidyCommission_4: str
    commission_5: str
    detail_id_5: str
    payTerm_5: str
    subsidyCommission_5: str
    commission_6: str
    detail_id_6: str
    payTerm_6: str
    subsidyCommission_6: str

class JsonDataModel(BaseModel):
    program_id: int
    product_id: int
    product_name: str
    data: str