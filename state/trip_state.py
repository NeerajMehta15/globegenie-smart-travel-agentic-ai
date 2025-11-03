from typing import Literal, Optional
from pydantic import BaseModel, Field
from db.models import UserProfile


class TripState(BaseModel):
    """
    Represents the state of a trip planning workflow.
    
    Phase 1: Basic trip planning (destination, itinerary, budget)
    Phase 2A: Personalized planning using user profiles and preferences
    """
    
    # ===== USER INPUT =====
    raw_input: str
    parsed_input: dict

    # ===== TRIP DETAILS =====
    destination: str
    duration: int
    budget: float
    dates: dict 
    number_of_travelers: int  
    trip_type: Literal["leisure", "business", "adventure", "cultural", "family", "romantic"]
    preferences: list[Literal["mountains", "beach", "city", "nature", "historical"]] 

    # ===== AGENT PROGRESS =====
    research_status: str
    itinerary_status: str
    budget_status: str
    
    # ===== LOOP MANAGEMENT =====
    current_loop: int
    max_loops: int
    convergence_score: float
    
    # ===== DECISIONS & RESULTS =====
    destination_research: dict
    itinerary_draft: dict
    budget_breakdown: dict
    final_plan: dict
    
    # ===== USER FEEDBACK =====
    user_satisfaction: Literal["very satisfied", "satisfied", "neutral", "dissatisfied", "very dissatisfied"]
    feedback_notes: str

    # =====  USER & PERSONALIZATION =====
    user_id: Optional[int] = None  
    user_profile: Optional[dict] = None 
    personalization_context: Optional[dict] = None 
    