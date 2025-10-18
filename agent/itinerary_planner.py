from core.llm_client import LLMClient
from core.prompt_library import load_prompt
from state.trip_state import TripState

class ItineraryPlanner:
    def __init__(self):
        self.llm_client = LLMClient()
        
    def plan(self, trip_state: TripState, optimization_context: dict = None) -> dict:
        print(f"[ITINERARY DEBUG] optimization_context received: {optimization_context}")
        
        # Extract data
        destination = trip_state.destination 
        preferences = trip_state.preferences
        trip_type = trip_state.trip_type
        duration = trip_state.duration
        budget = trip_state.budget
        destination_research = trip_state.destination_research
        
        # Prepare base input data
        input_data = {
            'destination': destination,
            'preferences': preferences,
            'trip_type': trip_type,
            'duration': duration,
            'budget': budget,
            'destination_research': destination_research
        }
        
        # Choose prompt based on optimization mode
        if optimization_context:
            print(f"[ITINERARY DEBUG] Using OPTIMIZATION mode")
            prompt = load_prompt('itinerary_optimization_prompt.txt') 
            input_data.update(optimization_context)
        else:
            print(f"[ITINERARY DEBUG] Using NORMAL mode")
            prompt = load_prompt('itinerary_planning_prompt.txt') 
        
        # Format and invoke LLM
        formatted_prompt = self.llm_client._format_prompt(prompt, input_data)
        response = self.llm_client.invoke(formatted_prompt)
        
        # Debug: Show raw response in optimization mode
        if optimization_context:
            print(f"[RAW RESPONSE] First 500 chars: {response[:500]}")
        
        # Parse response
        itinerary = self.llm_client._parse_json_response(response)

        # Debug: Check if cost decreased
        if optimization_context:
            print(f"[ITINERARY DEBUG] Parsed estimated_total_cost: {itinerary.get('estimated_total_cost', 'MISSING')}")
            if itinerary.get('estimated_total_cost') == optimization_context.get('current_cost'):
                print(f"[ITINERARY DEBUG] WARNING: Cost did NOT decrease!")

        return itinerary