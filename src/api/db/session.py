import sqlmodel
from sqlmodel import SQLModel, Session
#import timescaledb
from .config import settings
from sqlalchemy import text


if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

#engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)
engine = sqlmodel.create_engine(settings.DATABASE_URL)


def init_db():
    print("creating database")
    SQLModel.metadata.create_all(engine)
    #print("creating hypertables")
    #timescaledb.metadata.create_all(engine)
    print("Converting 'eventmodel' to hypertable") #converting manually cuz function "add_retention_policy" is not supported under the current "apache" license
    with Session(engine) as session:
        session.execute(
            text("""
                SELECT create_hypertable(
                    'eventmodel', 
                    'created_at', 
                    chunk_time_interval => INTERVAL '1 day',
                    if_not_exists => true
                );
            """)
        )
        session.commit()
        print("Hypertable created")

def get_session():
    with Session(engine) as session:
        yield session