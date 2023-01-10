from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn_string = 'postgres://user:superSecretPasswordThatShouldBeAnEnvVariable@localhost:5432/corteva-db'

engine = create_engine(conn_string)
# using a scoped session allows us to gracefully close connections when API request finish or the app shuts down
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Define the model Base object here - we are not going to subclass it, but we will use it for database creation
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import database.models
    Base.metadata.create_all(bind=engine)