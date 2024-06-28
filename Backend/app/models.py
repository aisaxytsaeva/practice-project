from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobAdd(BaseModel):
    name: str
    area: Optional[str] = None
    exp: Optional[str] = None
    sch: Optional[str] = None
    
    
class JobSchema(JobAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class JobId(BaseModel):
    ok: bool= True
    job_id: int