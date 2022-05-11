from blocker.database.interface import DataBaseBlockerInterface
from conf.db_session import create_session
from conf.models import WatchListIp


class DBWatchListIp(DataBaseBlockerInterface):
    def __init__(self):
        super(DBWatchListIp, self).__init__(database_model=WatchListIp)

    @staticmethod
    def count_occurrences(ipaddress: str) -> int:
        with create_session() as session:
            return session.query(WatchListIp).filter(WatchListIp.ip == ipaddress).count()

    @staticmethod
    def remove_observed_ip(ipaddress, system) -> None:
        with create_session() as session:
            results = session.query(WatchListIp).filter(WatchListIp.ip == ipaddress, WatchListIp.system == system).all()
            for result in results:
                session.delete(result)
            session.commit()
