from datetime import datetime
from typing import List

from blocker.database.interface import DataBaseBlockerInterface
from conf.db_session import create_session
from conf.models import BlockedIp


class DBBlockedIp(DataBaseBlockerInterface):
    """This class inherit from DataBaseBlockerInterface and create new methods
    to handle with blocked ips"""

    def __init__(self):
        super(DBBlockedIp, self).__init__(database_model=BlockedIp)

    @staticmethod
    def is_the_ip_blocked(ipaddress: str, system: str) -> bool:
        """This method check if an ip is blocked for a system"""

        with create_session() as session:
            result = session.query(BlockedIp).filter(BlockedIp.ip == ipaddress, BlockedIp.system == system).all()
            return True if result else False

    @staticmethod
    def list_blocked_ips(system: str = None) -> List[dict]:
        """This method list all blocked ips for a system"""

        with create_session() as session:
            results = session.query(BlockedIp).filter(BlockedIp.system == system).all() \
                if system else session.query(BlockedIp).all()
            return [{
                'ip': result.ip,
                'system': result.system,
                'date': datetime.fromisoformat(result.date)
            } for result in results]

    @staticmethod
    def remove_blocked_ip(ipaddress: str, system: str) -> None:
        """This method remove an ip from blocked ips list of a system"""

        with create_session() as session:
            results = session.query(BlockedIp).filter(BlockedIp.ip == ipaddress, BlockedIp.system == system).all()
            for result in results:
                session.delete(result)
            session.commit()
