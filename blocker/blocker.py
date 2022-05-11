from datetime import datetime
from typing import Optional, List

from blocker.database import DataBaseRequestIp, DataBaseBlockedIp


class Blocker:
    def __init__(
        self,
        ipaddress: str,
        system: str,
        limit_requests: int,
        limit_seconds: int,
        to_limit: bool = True,
        to_block: bool = False,
        to_limit_response: dict = None,
        to_block_response: dict = None,
        to_limit_database: DataBaseRequestIp = DataBaseRequestIp(),
        to_block_database: DataBaseBlockedIp = DataBaseBlockedIp(),
        show_time_left: bool = False
    ):
        self.ipaddress = ipaddress
        self.system = system
        self.limit_requests = limit_requests
        self.limit_seconds = limit_seconds
        self.to_block = to_block
        self.to_block_response = to_block_response
        self.to_block_database = to_block_database
        self.to_limit = to_limit
        self.to_limit_response = to_limit_response
        self.to_limit_database = to_limit_database
        self.show_time_left = show_time_left
        self.time_left: int = 0

    def __countdown(self, access_date: datetime) -> int:
        seconds_passed: int = (datetime.now() - access_date).total_seconds()
        time_left: int = self.limit_seconds - seconds_passed
        return round(time_left)

    def __to_limit_validate_access(self) -> bool:
        accesses: list = self.to_limit_database.fetch_requests(self.ipaddress)

        if len(accesses) < self.limit_requests:
            self.to_limit_database.save_new_request(self.ipaddress, self.system)
            return True

        latest_accesses: list = accesses[len(accesses) - self.limit_requests:]
        id_first_access: int = latest_accesses[0].id
        date_first_access: datetime = latest_accesses[0].date
        self.time_left: int = self.__countdown(date_first_access)

        if self.time_left <= 0:
            self.to_limit_database.remove_first_request(id_first_access)
            self.to_limit_database.save_new_request(self.ipaddress, self.system)
            return True

        return False

    def __to_block_validate_access(self) -> bool:
        valid_access: bool = self.__to_limit_validate_access()

        if not valid_access:
            self.to_block_database.save_new_request(self.ipaddress, self.system)

        return valid_access

    def __handle_to_limit(self) -> Optional[dict]:
        valid_access: bool = self.__to_limit_validate_access()

        if not valid_access:
            response: dict = self.to_limit_response

            if self.show_time_left:
                response.update({'time_left': self.time_left})

            return response

    def __handle_to_block(self) -> Optional[dict]:
        if self.to_block_database.is_the_ip_blocked(self.ipaddress):
            return self.to_block_response

        valid_access: bool = self.__to_block_validate_access()

        if not valid_access:
            return self.to_block_response

    def verify(self) -> dict:
        default = {"valid": True}

        if self.to_block:
            return self.__handle_to_block() or default

        elif self.to_limit:
            return self.__handle_to_limit() or default

        return default

    def list_blocked_ips(self, search_for_system_name: str) -> List[dict]:
        return self.to_block_database.list_blocked_ips(search_for_system_name)

    def remove_blocked_ip(self, ipaddress: str) -> None:
        return self.to_block_database.remove_blocked_ip(ipaddress)
