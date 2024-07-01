# from typing import Optional
from pydantic import BaseModel


class JobAdd(BaseModel):
    name: str
    sch: str
    
    
    
class JobSchema(JobAdd):
    id: int
    emp: str
    exp: str
    class Config:
        from_attributes = True


class JobId(BaseModel):
    ok: bool= True
    job_id: int