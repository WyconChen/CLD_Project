from pydantic import BaseModel

class ProgramModel(BaseModel):
    program_id: int = None
    program_name: str
    
class Baoyun18Model(BaseModel):
    program_id: int = None
    temp_id: int = None
    product_id: int = None
    product_name: str
    payDesc: str
    insureDesc: str
    first_rate: str
    second_rate: str