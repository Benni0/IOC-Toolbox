
from fastapi import APIRouter, Depends, Query


from app.utils.blacklist_lookups import get_listings
from app.utils.dns_lookups import get_ptr, get_a_record
from app.models import IP

from app.api_security import check_api_key

router = APIRouter(
    prefix="/ip",
    tags=['IP Service']
)

@router.get("/lookup/")
async def ipLookup(ip: str = Query(None, regex="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"), auth = Depends(check_api_key)):
    
    tags = get_listings(ip)
    
    ptr = get_ptr(ip)
    forward_lookup_match = False
    if ptr:
        forward = get_a_record(ptr)
        forward_lookup_match = ip in forward
            
    
    return IP(
        ip = ip,
        tags = tags,
        ptr = ptr,
        forward_lookup_match = forward_lookup_match
    )