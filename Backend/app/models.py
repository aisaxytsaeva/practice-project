from pydantic import BaseModel


class JobAdd(BaseModel):
    id: int
    name: str
    
class JobSchema(BaseModel):
    id: int
    name: str
    salary: int
    exp: str
    employ: str
    region: str