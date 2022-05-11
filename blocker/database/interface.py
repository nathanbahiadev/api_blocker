from abc import ABC
from typing import Union, List

from conf.db_session import create_session
from conf.models import RequestIp, BlockedIp


class DataBaseBlockerInterface(ABC):
    """This class implements the basic CRUD operations. It is abstract because we have
    three tables that have similar functions, and share the same code base looks like
    a good idea"""

    def __init__(self, database_model):
        self.database_model = database_model

    def fetch_requests(self, ipaddress: str) -> List[Union[RequestIp, BlockedIp]]:
        """List all results of an ipaddress in the database"""

        with create_session() as session:
            return session.query(RequestIp).where(self.database_model.ip == ipaddress).order_by(self.database_model.id).all()

    def remove_first_request(self, id_request: int) -> None:
        """Remove an element by id"""

        with create_session() as session:
            log = session.query(self.database_model).filter(self.database_model.id == id_request).one()
            session.delete(log)
            session.commit()

    def save_new_request(self, ipaddress: str, system: str) -> None:
        """Create a new line in the table"""

        with create_session() as session:
            request = self.database_model(ip=ipaddress, system=system)
            session.add(request)
            session.commit()
