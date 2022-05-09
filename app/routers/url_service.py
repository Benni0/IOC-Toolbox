from urllib.request import Request
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
import re

from app.models import LookupResult, UrlTrace, Domain, Url, LookupUrl
from app.routers.domain_service import domainLookup
from app.utils.url_trace import trace_url, UrlTracingException
from app.utils.domain_lookups import ALEXA_ONE_MILL, CISCO_UMBRELLA_ONE_MILL
from app.utils.dns_lookups import get_master

from app.api_security import check_api_key


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
async def traceUrlCall(lookup_url: LookupUrl, auth = Depends(check_api_key)):    
    trace = UrlTrace(
        base_url=lookup_url.url
    )
    
    domains = []
    for url, status_code in trace_url(lookup_url.url):
        trace.traced_urls.append(Url(url=url, status_code=status_code))
        domain = re.search("https?://([^/:]+).*", url)[1]
        domains.append(domain)

    print("test")
    for domain in set(domains):
        d = await domainLookup(domain, auth)
        trace.traced_domains.append(d)
        
    return trace