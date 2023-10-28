from typing import Optional
from pydantic import BaseModel


class UserInput(BaseModel):
    lon: Optional[float]
    lat: Optional[float]
    radius: Optional[float]


class Quote(BaseModel):
    character: str
    text: str


class SearchRequest(BaseModel):
    index_name: str
    search_dict: dict


class SearchUrl(BaseModel):
    url: str
