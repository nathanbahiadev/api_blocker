from datetime import datetime

from blocker.database.interface import DataBaseBlockerInterface
from conf.db_session import create_session
from conf.models import RequestIp


class DBRequestIp(DataBaseBlockerInterface):
    """This class inherit from DataBaseBlockerInterface and create new methods
    to handle with request ips"""

    def __init__(self):
        super(DBRequestIp, self).__init__(database_model=RequestIp)

    @staticmethod
    def remove_logs_ip(ipaddress: str, system: str) -> None:
        """This method remove an ip from request ips list of a system"""

        with create_session() as session:
            results = session.query(RequestIp).filter(RequestIp.ip == ipaddress, RequestIp.system == system).all()
            for result in results:
                session.delete(result)
            session.commit()

    @staticmethod
    def list_request_ips(system):
        """This method list all ips for a system"""

        with create_session() as session:
            results = session.query(RequestIp).filter(RequestIp.system == system).all() \
                if system else session.query(RequestIp).all()
            return [{
                'ip': result.ip,
                'system': result.system,
                'date': datetime.fromisoformat(result.date)
            } for result in results]
