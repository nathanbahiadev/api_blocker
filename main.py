from fastapi import FastAPI, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from blocker.post_data import Request as BlockerRequest, Ip
from blocker.blocker import Blocker
from conf.db_session import create_session

app = FastAPI(docs_url="/api/v1/documentation")

templates = Jinja2Templates(directory="templates")


@app.get("/{pk}", response_class=HTMLResponse)
async def dashboard(request: Request, system_name: str = None):
    with create_session() as session:
        blocked: list = Blocker.list_blocked_ips(search_for_system_name=system_name)
        last_results: list = Blocker.list_request_ips(search_for_system_name=system_name)

    context = {
        'request': request,
        'blocked': blocked,
        'last_results': last_results
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/api/v1/ip/verify/", status_code=status.HTTP_200_OK, tags=["IP"])
async def verify_access(request: BlockerRequest):
    """Main function - Receives the parameters and check is the request is valid"""
    response: dict = Blocker(**request.dict()).verify()
    return {"response": response}


@app.get("/api/v1/ip/blocked/", status_code=status.HTTP_200_OK, tags=["IP"])
async def blocked_ips(system_name: str = None):
    """Lists all blocked ips. Receives an optional query param 'system_name' to filter
    results by a specific system"""
    response: list = Blocker.list_blocked_ips(search_for_system_name=system_name)
    return {"response": response}


@app.post("/api/v1/ip/remove/", status_code=status.HTTP_204_NO_CONTENT, tags=["IP"])
async def remove_blocked_ip(ip: Ip):
    """Removes a blocked ip from the blocked and watch list by system"""
    Blocker(**ip.dict()).remove_blocked_ip()
    return


def custom_openapi():
    """Documentation settings"""

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
