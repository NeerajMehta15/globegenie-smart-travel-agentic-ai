from typing import Literal
from pydantic import BaseModel
from db.models import UserProfile


class TripState(BaseModel):
    """
    Represents the state of a trip, including its status, start and end times, and any relevant metadata.
    """
    # User input
    raw_input: str
    parsed_input: dict

    # Trip details
    destination: str
    duration: int
    budget: float
    dates: dict 
    number_of_travelers: int  
    trip_type: Literal["leisure", "business", "adventure", "cultural", "family", "romantic"]
    preferences: list[Literal["mountains", "beach", "city", "nature", "historical"]] 

    # Agent Progress
    research_status: str
    itinerary_status: str
    budget_status: str
    
    # Loop Management
    current_loop: int
    max_loops: int
    convergence_score: float
    
    # Decisions & Results
    destination_research: dict
    itinerary_draft: dict
    budget_breakdown: dict
    final_plan: dict
    
    # User Feedback
    user_satisfaction: Literal["very satisfied", "satisfied", "neutral", "dissatisfied", "very dissatisfied"]
    feedback_notes: str

    #User 
    user_id: Optional[int]
    user_profile: Optional[UserProfile]
    personalization_context: Optional[Dict]