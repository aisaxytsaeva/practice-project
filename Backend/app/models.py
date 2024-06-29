# from typing import Optional
from pydantic import BaseModel


class JobAdd(BaseModel):
    name: str
    
    
    
    
    
class JobSchema(BaseModel):
    id: int
    name: str
    sch: str
    emp: str
    exp: str


class JobId(BaseModel):
    ok: bool= True
    job_id: int