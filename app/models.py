from pydantic import BaseModel, constr
from typing import List, Optional


class Domain(BaseModel):
    domain: str
    tags:  List[str] = []
    dns_master: Optional[str]


class Url(BaseModel):
    url: str
    status_code: int
    tags:  List[str] = []
    

class IP(BaseModel):
    ip: str
    tags: List[str] = []
    ptr: Optional[str]
    forward_lookup_match: bool = False


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