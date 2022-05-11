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
