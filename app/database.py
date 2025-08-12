
# Import SQLAlchemy components needed for database setup and interaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL — here we store our file metadata locally in 'files.db' 
SQLALCHEMY_DATABASE_URL = "sqlite:///./files.db"

# Create the SQLAlchemy engine.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})# 'check_same_thread=False' is required for SQLite when using it with FastAPI,
# because FastAPI might handle requests in different threads.

# Create a session factory that will be used to talk to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all our ORM models. All models will inherit from this.
Base = declarative_base()

# Dependency function for FastAPI routes to get a DB session.
#Here each request has its own session and it will be closed after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
