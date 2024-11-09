from pydantic import BaseModel

class NoOp(BaseModel):
    data: str
