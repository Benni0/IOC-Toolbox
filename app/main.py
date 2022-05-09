from logging import exception
from fastapi import FastAPI
from app.routers import domain_service, ip_service, url_service

app = FastAPI()


for ex_class, exception_handler in url_service.exception_handers:
    app.add_exception_handler(ex_class, exception_handler)


app.include_router(domain_service.router)
app.include_router(ip_service.router)
app.include_router(url_service.router)
