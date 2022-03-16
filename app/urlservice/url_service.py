from urllib.request import Request
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
import re

from .models import LookupResult, UrlTrace, Domain, Url, LookupUrl
from .utils.url_trace import trace_url, UrlTracingException
from .utils.domain_lookups import ALEXA_ONE_MILL, CISCO_UMBRELLA_ONE_MILL
from .utils.dns_lookups import get_master

from ..api_security import check_api_key


router = APIRouter(
    prefix="/url",
    tags=['URL Service']
)

async def url_tracing_exception_handler(reqest: Request, e: UrlTracingException):
    return JSONResponse(
        status_code=424,
        content={"message": e.message}
    )

exception_handers = [(UrlTracingException, url_tracing_exception_handler)]

@router.post("/calltrace", response_model=UrlTrace )
async def traceUrlCall(
    lookup_url: LookupUrl,
    enable_tagging: bool = False, 
    auth = Depends(check_api_key)):
    
    trace = UrlTrace(
        base_url=lookup_url.url
    )
    
    domains = []
    for url, status_code in trace_url(lookup_url.url):
        trace.traced_urls.append(Url(url=url, status_code=status_code))
        domain = re.search("https?://([^/:]+).*", url)[1]
        domains.append(domain)

    for domain in set(domains):
        d = Domain(domain=domain)
            
        if enable_tagging:
            dns_master = get_master(domain)
            domain_in_alexa = ALEXA_ONE_MILL.lookup_domain(domain)
            domain_in_umbrella = CISCO_UMBRELLA_ONE_MILL.lookup_domain(domain)
            if dns_master: d.tags.append(f"dns:{dns_master}")
            if domain_in_alexa: d.tags.append("ALEXA_ONE_MILL")
            if domain_in_umbrella: d.tags.append("CISCO_UMBRELLA_ONE_MILL")
            
        trace.traced_domains.append(d)
    return trace


@router.get("/lookup/alexa")
async def urlLookup(domain: str, auth = Depends(check_api_key)):
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
async def urlLookup(domain: str, auth = Depends(check_api_key)):
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
