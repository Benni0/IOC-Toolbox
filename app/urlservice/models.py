from pydantic import BaseModel, constr
from typing import List


class Domain(BaseModel):
    domain: str
    tags:  List[str] = []


class Url(BaseModel):
    url: str
    status_code: int
    tags:  List[str] = []


class UrlTrace(BaseModel):
    base_url: str 
    traced_urls: List[Url] = []
    traced_domains: List[Domain] = []


class LookupResult(BaseModel):
    domain: str
    is_in_list: bool
    rank: int = 0
    
class LookupUrl(BaseModel):
    url: constr(regex=r'^https?://.*$')