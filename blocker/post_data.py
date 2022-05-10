from pydantic import BaseModel


class Request(BaseModel):
    ipaddress: str
    system: str
    limit_requests: int = 10
    limit_seconds: int = 60
    to_limit: bool = False
    to_block: bool = False
    to_limit_response: dict = {}
    to_block_response: dict = {}
    show_time_left: bool = False


class Ip(BaseModel):
    ipaddress: str
