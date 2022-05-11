from datetime import datetime

from sqlalchemy import Column, Integer, String

from conf.model_base import ModelBase


def datetime_to_iso() -> str:
    return datetime.now().isoformat()


class RequestIp(ModelBase):
    __tablename__ = 'ips'
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ip: str = Column(String, nullable=False)
    date: str = Column(String, default=datetime_to_iso)
    system: str = Column(String, nullable=False)


class BlockedIp(ModelBase):
    __tablename__ = 'blocked_ips'
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ip: str = Column(String, nullable=False)
    date: str = Column(String, default=datetime_to_iso)
    system: str = Column(String, nullable=False)


class WatchListIp(ModelBase):
    __tablename__ = 'watch_list_ips'
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ip: str = Column(String, nullable=False)
    date: str = Column(String, default=datetime_to_iso)
    system: str = Column(String, nullable=False)
