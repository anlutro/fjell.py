import diay
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import sqlalchemy.orm.session
import sqlalchemy.ext.declarative

from fjell.config import Config


__plugin__ = 'SqlAlchemyPlugin'


class SqlAlchemyPlugin(diay.Plugin):
    @diay.provider(singleton=True)
    def provide_db_engine(self, config: Config) -> sqlalchemy.engine.Engine:
        return sqlalchemy.create_engine(config.get('db'), convert_unicode=True)

    @diay.provider(singleton=True)
    def provide_session(self, engine: sqlalchemy.engine.Engine) -> sqlalchemy.orm.session.Session:
        return sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.session.sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )


Base = sqlalchemy.ext.declarative.declarative_base()


@diay.inject('session', sqlalchemy.orm.session.Session)
class SqlAlchemyMixin:
    pass
