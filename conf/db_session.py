"""This module is responsible for the database settings"""


from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session, sessionmaker
from decouple import config

from conf.models import ModelBase


__engine: Optional[Engine] = None
__str_conn = config('DATABASE_URL')


def __create_engine() -> Engine:
    """Configure the database engine"""

    global __engine

    if not __engine:
        __engine = create_engine(url=__str_conn, echo=False)

    return __engine


def create_session() -> Session:
    """Create the session responsible for the database operations"""

    global __engine

    if not __engine:
        __engine = __create_engine()

    __session: callable = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    session: Session = __session()
    return session


def create_tables() -> None:
    """Drop and create new tables"""

    print("Iniciando criação do banco de dados...")

    global __engine

    if not __engine:
        __engine = __create_engine()

    # The import below is necessary to sqlalchemy recognize the declared models
    from conf import all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)

    print("Banco de dados criado com sucesso!")
