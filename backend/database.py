"""
Database configuration and connection setup for PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine
# The engine is the core interface to the database
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    echo=True  # Log all SQL statements (useful for debugging)
)

# Create a SessionLocal class
# Each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
# All database models will inherit from this
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency that creates a new database session for each request
    and closes it when the request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
