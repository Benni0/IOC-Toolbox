from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.models import LookupResult, Domain
from app.utils.domain_lookups import ALEXA_ONE_MILL, CISCO_UMBRELLA_ONE_MILL
from app.utils.dns_lookups import get_master

from app.api_security import check_api_key


router = APIRouter(
    prefix="/domain",
    tags=['Domain Service']
)


@router.get("/lookup/")
async def domainLookup(domain: str, auth = Depends(check_api_key)):
    lists = {
        'CISCO_UMBRELLA_ONE_MILL': CISCO_UMBRELLA_ONE_MILL,
        'ALEXA_ONE_MILL': ALEXA_ONE_MILL,
    }
    
    tags = []
    for list_name in lists:
        lookup_result = lists[list_name].lookup_domain(domain)    
        if lookup_result is not None:
            tags.append(list_name)
            
    dns_master = get_master(domain)
    return Domain(
        domain=domain,
        tags = tags,
        dns_master = dns_master
    )


@router.get("/lookup/alexa")
async def urlLookupAlexa(domain: str, auth = Depends(check_api_key)):
    lookup_result = ALEXA_ONE_MILL.lookup_domain(domain)
    if lookup_result is not None:
        return LookupResult(
            domain=domain,
            is_in_list=True,
            rank=lookup_result[1]
        )
    else:
        return LookupResult(
            domain=domain,
            is_in_list=False
        )

@router.get("/lookup/umbrella")
async def urlLookupUmbrella(domain: str, auth = Depends(check_api_key)):
    lookup_result = CISCO_UMBRELLA_ONE_MILL.lookup_domain(domain)
    if lookup_result is not None:
        return LookupResult(
            domain=domain,
            is_in_list=True,
            rank=lookup_result[1]
        )
    else:
        return LookupResult(
            domain=domain,
            is_in_list=False
        )
