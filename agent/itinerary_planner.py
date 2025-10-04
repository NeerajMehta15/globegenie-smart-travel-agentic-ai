from core.llm_client import LLMClient
from core.prompt_library import load_prompt
from state.trip_state import TripState

class ItineraryPlanner:
    def __init__(self):
        self.llm_client = LLMClient()
        
    def plan(self, trip_state: TripState) -> list:
        # Extract data from trip_state
        destination = trip_state.destination 
        preferences = trip_state.preferences
        trip_type = trip_state.trip_type
        duration = trip_state.duration
        budget = trip_state.budget
        destination_research = trip_state.destination_research
        
        # Load itinerary prompt
        prompt = load_prompt('itinerary_planning_prompt.txt')
        
        # Prepare input data
        input_data = {
            'destination': destination,
            'preferences': preferences,
            'trip_type': trip_type,
            'duration': duration,
            'budget': budget,
            'destination_research': destination_research
        }
        
        # Format and invoke LLM
        formatted_prompt = self.llm_client._format_prompt(prompt, input_data)
        response = self.llm_client.invoke(formatted_prompt)
        
        # Parse and return itinerary list
        itinerary = self.llm_client._parse_json_response(response)
        
        return itinerary