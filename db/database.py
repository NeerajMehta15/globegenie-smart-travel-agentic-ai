'''Database connection and base model setup
    - Engine: Connect to the database
    - SessionLocal: Create session factory for database interactions
    - Base: Declarative base for model definitions
    - get_db: Dependency to provide database sessions
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

#======== Database Configuration ========#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "globegenie.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

#======== Create Engine =================#
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Enable SQL query logging for debugging
    connect_args={"check_same_thread": False},  # SQLite specific argument
    poolclass=StaticPool) # Use StaticPool for SQLite to avoid threading issues

#======== Create Session Factory =======#
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

#======== Base - Parent class for models =======#
Base = declarative_base()

#======== Helper function to get DB session =======#
def get_db():
    """
    Dependency function that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    
    Note:
        - Safe to call multiple times (won't recreate existing tables)
        - Only creates tables that don't exist
        - Doesn't modify existing tables or data
    """
    # Import models here to ensure they're registered with Base
    from db.models import User, UserProfile, TripHistory
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print(f"Database initialized at: {DATABASE_PATH}")
    print(f"Tables created: users, user_profiles, trip_history")

def drop_all_tables():
    """
    DANGER: Drops all tables from the database.
    """
    Base.metadata.drop_all(bind=engine)
    print(f"🗑️  All tables dropped from: {DATABASE_PATH}")

def reset_db():
    """
    Reset the database by dropping and recreating all tables.
    """
    print("Resetting database...")
    drop_all_tables()
    init_db()
    print("Database reset complete!")

#===========DATABASE INFO HELPER==================#

def get_db_info():
    """
    Get information about the database.
    
    Returns:
        dict: Database information including path, size, and table count
    """
    info = {
        "path": DATABASE_PATH,
        "exists": os.path.exists(DATABASE_PATH),
        "size_bytes": os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0,
    }
    
    # Get table names if database exists
    if info["exists"]:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        info["tables"] = inspector.get_table_names()
        info["table_count"] = len(info["tables"])
    else:
        info["tables"] = []
        info["table_count"] = 0
    
    return info

# Check if database exists on module import
if not os.path.exists(DATABASE_PATH):
    print(f"Database not found at: {DATABASE_PATH}")
    print(f"Run init_db() to create the database")
else:
    db_size = os.path.getsize(DATABASE_PATH)
    print(f"Database found at: {DATABASE_PATH} ({db_size} bytes)")