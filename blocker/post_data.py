from pydantic import BaseModel


class Request(BaseModel):
    ipaddress: str
    system: str
    to_limit: bool
    to_block: bool
    limit_seconds: int = 60
    limit_requests: int = 10
    to_limit_response: dict = {}
    to_block_response: dict = {}
    show_time_left: bool = False


class Ip(BaseModel):
    ipaddress: str
