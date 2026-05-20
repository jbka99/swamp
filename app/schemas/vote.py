from pydantic import BaseModel

class VoteCreate(BaseModel):
    value: int