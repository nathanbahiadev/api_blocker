from datetime import datetime
from typing import Optional, List

from blocker.database.request_ip import DBRequestIp
from blocker.database.blocked_ip import DBBlockedIp
from blocker.database.watch_list import DBWatchListIp


class Blocker:
    to_limit_database: DBRequestIp = DBRequestIp()
    to_block_database: DBBlockedIp = DBBlockedIp()
    watch_database: DBWatchListIp = DBWatchListIp()

    def __init__(
        self,
        system: str,
        ipaddress: str,
        to_limit: bool = True,
        to_block: bool = False,
        limit_seconds: int = 60,
        limit_requests: int = 10,
        occurrences_to_block: int = 1,
        to_limit_response: dict = None,
        to_block_response: dict = None,
    ):
        self.limited = False
        self.blocked = False
        self.system = system
        self.time_left: int = 0
        self.to_limit = to_limit
        self.to_block = to_block
        self.count_occurrences = 0
        self.ipaddress = ipaddress
        self.limit_seconds = limit_seconds
        self.limit_requests = limit_requests
        self.to_limit_response = to_limit_response
        self.to_block_response = to_block_response
        self.occurrences_to_block = occurrences_to_block

    def __countdown(self, access_date: datetime) -> int:
        """This method calculates the time left to a new request according to
        limit_requests and limit_seconds parameters"""

        seconds_passed: int = (datetime.now() - access_date).total_seconds()
        time_left: int = self.limit_seconds - seconds_passed
        return round(time_left)

    def __to_limit_validate_access(self) -> bool:
        """This method check if the request is valid and change the value of some
        properties, like self.limited and self.blocked"""

        # Fetch all results of ip address
        accesses: list = self.to_limit_database.fetch_requests(self.ipaddress)

        # Check if the quantity of logs is greater than the self.limit_requests
        if len(accesses) < self.limit_requests:
            self.to_limit_database.save_new_request(self.ipaddress, self.system)
            self.limited = False
            return self.limited

        latest_accesses: list = accesses[len(accesses) - self.limit_requests:]

        # Check if it's the first access of an ip address
        if not latest_accesses:
            self.to_limit_database.save_new_request(self.ipaddress, self.system)
            self.limited = False
            return self.limited

        # Calcula the time passed from the first access to now and check if the
        # request is valid
        id_first_access: int = latest_accesses[0].id
        date_first_access: datetime = datetime.fromisoformat(latest_accesses[0].date)
        self.time_left: int = self.__countdown(date_first_access)

        if self.time_left <= 0:
            self.to_limit_database.remove_first_request(id_first_access)
            self.to_limit_database.save_new_request(self.ipaddress, self.system)
            self.limited = False
            return self.limited

        self.limited = True
        return self.limited

    def __to_block_validate_access(self) -> bool:
        """This method check if the request is valid and increase the property
        self.count_occurrences. If the self.count_occurrences is greater than
        self.occurrences_to_block, the ip address is added to a list of blocked
        ips. count_occurrences represents every time the request was limited by
        the Blocker"""

        self.__to_limit_validate_access()

        self.count_occurrences = self.watch_database.count_occurrences(self.ipaddress)

        # Count of occurrences and block the ip if applicable
        if self.count_occurrences >= self.occurrences_to_block:
            self.to_block_database.save_new_request(self.ipaddress, self.system)
            self.blocked = True

        # Is the request was limited, the number os occurrences must be increased by 1
        # and the ip address placed on a watch list
        if self.limited:
            self.count_occurrences += 1
            self.watch_database.save_new_request(self.ipaddress, self.system)

        return self.blocked

    def __handle_to_limit(self) -> Optional[dict]:
        """This method handles the operation of limiting requests and return a
        response to the main method"""
        self.__to_limit_validate_access()
        response: dict = self.to_limit_response

        if self.limited:
            response.update({'limited': True})
            if self.time_left > 0:
                response.update({'time_left': self.time_left})
            return response

    def __handle_to_block(self) -> Optional[dict]:
        """This method handles the operation of blocking requests and return a
        response to the main method"""

        response = self.to_block_response

        if self.to_block_database.is_the_ip_blocked(self.ipaddress, self.system):
            response.update({'blocked': True})
            return response

        self.__to_block_validate_access()

        if self.blocked:
            response.update({'blocked': self.blocked})
            return response

        if self.limited:
            response = self.to_limit_response
            response.update({'limited': self.limited})
            response.update({'time_left': self.time_left})
            response.update({'occurrences': self.count_occurrences})
            return response

    def verify(self) -> dict:
        """The main method"""

        default = {"valid": True}

        if self.to_block:
            return self.__handle_to_block() or default

        elif self.to_limit:
            return self.__handle_to_limit() or default

        return default

    @classmethod
    def list_blocked_ips(cls, search_for_system_name: str) -> List[dict]:
        """This method does what it's name describes, duhh"""
        return cls.to_block_database.list_blocked_ips(search_for_system_name)

    def remove_blocked_ip(self) -> None:
        """This method does what it's name describes, duhh"""
        self.to_block_database.remove_blocked_ip(self.ipaddress, self.system)
        self.to_limit_database.remove_logs_ip(self.ipaddress, self.system)
        self.watch_database.remove_observed_ip(self.ipaddress, self.system)
