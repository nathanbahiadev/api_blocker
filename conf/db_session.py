from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session, sessionmaker
from decouple import config

from conf.models import ModelBase


__engine: Optional[Engine] = None
__str_conn = config('DATABASE_URL')


def __create_engine() -> Engine:
    global __engine

    if not __engine:
        __engine = create_engine(url=__str_conn, echo=False)

    return __engine


def create_session() -> Session:
    global __engine

    if not __engine:
        __engine = __create_engine()

    __session: callable = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    session: Session = __session()
    return session


def create_tables() -> None:
    global __engine

    if not __engine:
        __engine = __create_engine()

    from conf import all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
