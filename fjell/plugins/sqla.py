import diay
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from fjell.config import Config


__plugin__ = 'SqlAlchemyPlugin'


class SqlAlchemyPlugin(diay.Plugin):
    @diay.provider(singleton=True)
    def provide_db_engine(self, config: Config) -> Engine:
        return sqlalchemy.create_engine(config.get('db'), convert_unicode=True)

    @diay.provider(singleton=True)
    def provide_session(self, engine: Engine) -> Session:
        return sqlalchemy.orm.scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )


Base = sqlalchemy.ext.declarative.declarative_base()


@diay.inject('session', Session)
class SqlAlchemyMixin:
    pass
