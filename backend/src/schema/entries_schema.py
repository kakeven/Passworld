from pydantic import BaseModel

class Entry(BaseModel):
    service:str 
    login:str
    password:str