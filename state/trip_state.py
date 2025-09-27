from pydantic import BaseModel

class TripState(BaseModel):
    """
    Represents the state of a trip, including its status, start and end times, and any relevant metadata.
    """
    #User input
    raw_input : str
    parsed_input : dict

    #Trip details
    destination : str
    duration : int
    budget : float
    dates : dict 
    number_of_travelers : list
    Trip_type : Literal["leisure", "business", "adventure", "cultural", "family", "romantic"]
    preferences : Literal["moutains", "beach", "city", "nature", "historical"]

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
    itinerary_draft: list
    budget_breakdown: dict
    final_plan: dict
    
    # User Feedback
    user_satisfaction: Literal["very satisfied", "satisfied", "neutral", "dissatisfied", "very dissatisfied"]
    feedback_notes: str
