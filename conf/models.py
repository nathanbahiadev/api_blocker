from datetime import datetime

from sqlalchemy import Column, Integer, String, DATETIME, Boolean

from conf.model_base import ModelBase


class RequestIp(ModelBase):
    __tablename__ = 'ips'
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ip: str = Column(String, nullable=False)
    date: datetime = Column(DATETIME, default=datetime.now)
    system: str = Column(String, nullable=False)


class BlockedIp(ModelBase):
    __tablename__ = 'blocked_ips'
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ip: str = Column(String, nullable=False)
    date: datetime = Column(DATETIME, default=datetime.now)
    system: str = Column(String, nullable=False)
