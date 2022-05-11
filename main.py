from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi

from blocker.post_data import Request, Ip
from blocker.blocker import Blocker


app = FastAPI(docs_url="/api/v1/documentation")


@app.post("/api/v1/ip/verify/", status_code=status.HTTP_200_OK, tags=["IP"])
async def verify_access(request: Request):
    response: dict = Blocker(**request.dict()).verify()
    return {"response": response}


@app.get("/api/v1/ip/blocked/", status_code=status.HTTP_200_OK, tags=["IP"])
async def blocked_ips(system_name: str = None):
    response: list = Blocker.list_blocked_ips(search_for_system_name=system_name)
    return {"response": response}


@app.post("/api/v1/ip/remove/", status_code=status.HTTP_204_NO_CONTENT, tags=["IP"])
async def remove_blocked_ip(ip: Ip):
    ipaddress: str = ip.ipaddress
    Blocker.remove_blocked_ip(ipaddress)
    return {}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Blocker",
        version="0.0.1",
        description="API Blocker - Um micro-serviço para restrição de requisições",
        routes=app.routes,
        contact={
            "name": "Nathan Bahia",
            "email": "nathan@unidasolucoes.com.br",
            "url": "https://linkedin.com/in/nathanbahia"
        },
        tags=[
            {"name": "IP"}
        ]
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
