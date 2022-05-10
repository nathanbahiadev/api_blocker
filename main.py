from fastapi import FastAPI, status

from blocker.post_data import Request, Ip
from blocker.blocker import Blocker
from blocker.database import DataBaseBlockedIp


app = FastAPI()


@app.post("/ip/verify/")
async def verify_access(request: Request):
    response: dict = Blocker(**request.dict()).verify()
    return {"response": response}


@app.get("/ip/blocked/")
async def blocked_ips(system: str = None):
    response: list = DataBaseBlockedIp.list_blocked_ips(system)
    return {"response": response}


@app.post("/ip/remove/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_blocked_ip(ip: Ip):
    DataBaseBlockedIp.remove_blocked_ip(ip.ipaddress)
    return {}
