from abc import ABC
from typing import Union, List

from conf.db_session import create_session
from conf.models import RequestIp, BlockedIp


class DataBaseBlockerInterface(ABC):
    def __init__(self, database_model):
        self.database_model = database_model

    def fetch_requests(self, ipaddress: str) -> List[Union[RequestIp, BlockedIp]]:
        with create_session() as session:
            return session.query(RequestIp).where(self.database_model.ip == ipaddress).order_by(self.database_model.id).all()

    def remove_first_request(self, id_request: int) -> None:
        with create_session() as session:
            log = session.query(self.database_model).filter(self.database_model.id == id_request).one()
            session.delete(log)
            session.commit()

    def save_new_request(self, ipaddress: str, system: str) -> None:
        with create_session() as session:
            request = self.database_model(ip=ipaddress, system=system)
            session.add(request)
            session.commit()


class DataBaseRequestIp(DataBaseBlockerInterface):
    def __init__(self):
        super(DataBaseRequestIp, self).__init__(database_model=RequestIp)


class DataBaseBlockedIp(DataBaseBlockerInterface):
    def __init__(self):
        super(DataBaseBlockedIp, self).__init__(database_model=BlockedIp)

    @staticmethod
    def is_the_ip_blocked(ipaddress) -> bool:
        with create_session() as session:
            return True if session.query(BlockedIp).filter(BlockedIp.ip == ipaddress).all() else False

    @staticmethod
    def list_blocked_ips(system: str = None) -> List[dict]:
        with create_session() as session:
            results = session.query(BlockedIp).filter(BlockedIp.system == system).all() \
                if system else session.query(BlockedIp).all()
            return [{'ip': result.ip, 'system': result.system, 'date': result.date} for result in results]

    @staticmethod
    def remove_blocked_ip(ipaddress: str) -> None:
        with create_session() as session:
            results = session.query(BlockedIp).filter(BlockedIp.ip == ipaddress).all()
            for result in results:
                session.delete(result)
            session.commit()
