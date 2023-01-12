from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn_string = "postgresql://postgres:password@localhost:5432/corteva-db"

engine = create_engine(conn_string)
# using a scoped session allows us to gracefully close connections when API request finish or the app shuts down
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
