
# db/__init__.py

"""
GlobeGenie Database Package

This package provides database models, CRUD operations, and connection management
for the GlobeGenie travel planning system.

Usage:
    from db import SessionLocal, User, create_user_with_profile
    
    db = SessionLocal()
    user, profile = create_user_with_profile(db, "john@example.com", "John")
    db.close()
"""

# Import database components
from db.database import (
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db,
    reset_db,
    get_db_info
)

# Import models
from db.models import (
    User,
    UserProfile,
    TripHistory,
    TRAVEL_STYLES,
    BUDGET_RANGES,
    PACE_PREFERENCES,
    INTEREST_CATEGORIES
)

# Import CRUD operations
from db.crud import (
    # User management
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    user_exists,
    
    # Profile management
    create_user_profile,
    get_user_profile,
    update_user_profile,
    create_user_with_profile,
    
    # Trip history
    save_trip_history,
    get_user_trips,
    get_trip_by_id,
    update_trip_feedback
)

__all__ = [
    # Database
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "init_db",
    "reset_db",
    "get_db_info",
    
    # Models
    "User",
    "UserProfile",
    "TripHistory",
    "TRAVEL_STYLES",
    "BUDGET_RANGES",
    "PACE_PREFERENCES",
    "INTEREST_CATEGORIES",
    
    # CRUD
    "create_user",
    "get_user_by_id",
    "get_user_by_email",
    "get_all_users",
    "user_exists",
    "create_user_profile",
    "get_user_profile",
    "update_user_profile",
    "create_user_with_profile",
    "save_trip_history",
    "get_user_trips",
    "get_trip_by_id",
    "update_trip_feedback",
]