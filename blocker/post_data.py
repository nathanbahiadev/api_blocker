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
    occurrences_to_block: int = 1


class Ip(BaseModel):
    ipaddress: str
    system: str
