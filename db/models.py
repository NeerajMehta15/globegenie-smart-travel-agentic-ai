from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

#Predefined constants
TRAVEL_STYLES = ["luxury", "budget", "backpacker", "balanced"]
BUDGET_RANGES = ["low", "medium", "high"] 
PACE_PREFERENCES = ["relaxed", "moderate", "packed"]

#This is part of the Tripstate class
INTEREST_CATEGORIES = [
    "beach",
    "culture", 
    "adventure",
    "food",
    "nightlife",
    "nature",
    "shopping",
    "history",
    "wellness",
    "photography"
]

#Class for basic account information
class User:
    '''Database model for User accounts'
    
    One user has: 
    - One profile
    - Many trip states
    '''

     __tablename__ = "users"
    
    #Primary identifier for each users and other column details
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True, index=True, nullable=False) #Nullable false to ensure email is always provided, index = True for faster lookups
    name = Column(String, nullable=False)
    home_city = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #Relationships,One-to-One with UserProfile, One-to-Many with TripState,userlist=False for only one profile per user,back_populates to link both sides of relationship,cascade to delete profile when user is deleted
    profile = relationship("UserProfile", 
                            back_populates="user",
                            uselist=False,
                            cascade="all, delete-orphan")

    #One-to-Many relationship with TripState
    trip_history = relationship("TripHistory",
                                back_populates="user",
                                cascade="all, delete-orphan")
    
    def __repr__(self):
       '''String representation of debugging purposes'''
       return f"<User(id={self.id}, email={self.email}, name={self.name})>"

# TRIP HISTORY MODEL - Past trips for learning and reference
class TripHistory(Base):
   '''Store past trip details for users'''

   #Table name
   __tablename__ = "trip_history" 

   #Linking to user table
   id = Column(Integer, primary_key=True, index=True)
   user_id = Column(Integer,ForeignKey("users.id"), nullable=False)

   #=============Trip details==================
   destination = Column(String, nullable=False)
   trip_dates = Column(JSON, nullable=False)        #Storing start and end dates as JSON
   duration_days = Column(Integer, nullable=False)  #Duration in days
   num_travelers = Column(Integer, nullable=False)  #Number of travelers

   #=============Budget tracking===============
   budget_target = Column(Float,nullable=False)     #Planned budget
   total_cost = Column(Float,nullable=True)         #Actual amount spent
   within_budget = Column(Boolean,nullable=True)    #Whether trip was within budget

   # ============Full trip data================
   trip_data = Column(JSON, nullable=True)          #Storing full trip details as JSON for reference
   acitivity_summary = Column(Text, nullable=True)  #Summary of activities done during trip
   destination_info = Column(JSON, nullable=True)   #Storing destination info as JSON

   # =============User feedback================
   feedback_rating = Column(Text, nullable=True)         #User feedback on trip
   feedback_text = Column(Text, nullable=True)           #Detailed feedback text
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())

   #=============Relationships==================
   user = relationship("User", back_populates="trip_history")

   def __repr__(self):
       '''String representation for debugging purposes'''
       return f"<TripHistory(id={self.id}, user_id={self.user_id}, destination={self.destination})>"
   

