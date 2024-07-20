from pydantic import BaseModel


class ResponseInfo(BaseModel):
    details: str
