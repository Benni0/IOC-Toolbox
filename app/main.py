from logging import exception
from fastapi import FastAPI, Depends
from app.routers import domain_service, ip_service, url_service
from app.api_security import check_api_key
from app.models import Success

app = FastAPI()


@app.get('/connectivitytest')
def test_connectivity(auth = Depends(check_api_key)):
    return Success(
        state="success"
    )


for ex_class, exception_handler in url_service.exception_handers:
    app.add_exception_handler(ex_class, exception_handler)


app.include_router(domain_service.router)
app.include_router(ip_service.router)
app.include_router(url_service.router)
