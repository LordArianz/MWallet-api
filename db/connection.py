from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import CONFIGURATION

engine = create_engine('postgresql+pg8000://' + CONFIGURATION["POSTGRE_USERNAME"] + ':' + CONFIGURATION["POSTGRE_PASSWORD"] + '@127.0.0.1/' + CONFIGURATION["POSTGRE_DB"], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import db.models
    #print Base.metadata.tables
    Base.metadata.create_all(bind=engine)
    print 'db_connected'
