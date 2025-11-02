"""
CRUD (Create, Read, Update, Delete) operations for GlobeGenie database.

This module provides reusable functions for database operations:
- User management (create, read users)
- Profile management (create, update preferences)
- Trip history (save, retrieve trips)
- Analytics (search, patterns)
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List, Dict
from datetime import datetime

from db.models import User, UserProfile, TripHistory

#=============== SECTION 1: USER MANAGEMENT - BASIC INFORMATION ===============#

def create_user(db: Session, email: str, name: str, home_city: Optional[str] = None) -> User:
    """Create a new user in the database."""
    try:
        user = User(email=email, name=name, home_city=home_city)
        db.add(user) #Add to session
        db.commit()  #save to database
        db.refresh(user) #Refresh to get updated fields like id
        return user
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email."""
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Retrieve all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

#=============== SECTION 2: USER PROFILE MANAGEMENT - TRAVEL PREFERENCES ===============#

def create_user_profile(db: Session, user_id: int, travel_style: str, budget_range: str, pace_preference: str, interests: List[str]) -> UserProfile:
    """Create a user profile with travel preferences."""
    try:
        profile = UserProfile(
            user_id=user_id,
            travel_style=travel_style,
            budget_range=budget_range,
            pace_preference=pace_preference,
            interests=interests
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    except Exception as e:
        db.rollback()
        raise e
    
def get_user_profile(db: Session, user_id: int) -> Optional[UserProfile]:
    """Retrieve a user's profile by user ID."""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

def update_user_profile(db: Session,user_id: int,travel_style: Optional[str] = None, budget_range: Optional[str] = None,pace_preference: Optional[str] = None,
                        interests: Optional[List[str]] = None) -> Optional[UserProfile]:
    """
    Update a user's profile preferences.
    """
    profile = get_user_profile(db, user_id)
    
    if not profile:
        return None
    
    try:
        # Only update fields that are provided
        if travel_style is not None:
            profile.travel_style = travel_style
            
        if budget_range is not None:
            profile.budget_range = budget_range
            
        if pace_preference is not None:
            profile.pace_preference = pace_preference
            
        if interests is not None:
            profile.interests = interests
        
        db.commit()
        db.refresh(profile)
        
        return profile
        
    except Exception as e:
        db.rollback()
        raise e

def create_user_with_profile( db: Session, email: str, name: str, home_city: Optional[str] = None,travel_style: str = "balanced",
                             budget_range: str = "medium", pace_preference: str = "moderate", interests: Optional[List[str]] = None) -> tuple[User, UserProfile]:
    """
    Convenience function: Create user and profile in one go.
    
    This is the most common operation - when a new user signs up,
    we will create both their account and profile together.
    
    """
    try:
        # Create user first
        user = create_user(db, email, name, home_city)
        
        # Then create profile
        profile = create_user_profile(
            db,
            user_id=user.id,
            travel_style=travel_style,
            budget_range=budget_range,
            pace_preference=pace_preference,
            interests=interests
        )
        
        return user, profile
        
    except Exception as e:
        db.rollback()
        raise e

#=============== SECTION 3: TRIP HISTORY - Save and retrieve trips ===============#




#============== HELPER FUNCTIONS ==============#
def user_exists(db: Session, email: str) -> bool:
    """
    Check if a user with this email already exists.
    
    Useful for: Validation before creating new user.
    """
    return db.query(User).filter(User.email == email).first() is not None