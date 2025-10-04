from core.llm_client import LLMClient
from core.prompt_library import load_prompt
from state.trip_state import TripState

class BudgetAnalyzer:
    def __init__(self):
        self.llm_client = LLMClient()
        
    def analyze_budget(self, trip_state: TripState) -> dict:
        # Extract data
        destination = trip_state.destination 
        duration = trip_state.duration
        budget = trip_state.budget
        destination_research = trip_state.destination_research
        itinerary_draft = trip_state.itinerary_draft
        number_of_travelers = trip_state.number_of_travelers 
        
        # Load budget prompt
        prompt = load_prompt('budget_analysis_prompt.txt')
        
        # Format and invoke LLM
        input_data = {
            'destination': destination,
            'duration': duration,
            'budget': budget,
            'destination_research': destination_research,
            'itinerary_draft': itinerary_draft,
            'number_of_travelers' : number_of_travelers 
        }
        formatted_prompt = self.llm_client._format_prompt(prompt, input_data)
        response = self.llm_client.invoke(formatted_prompt)
        
        # Parse and return budget breakdown dict
        budget_breakdown = self.llm_client._parse_json_response(response)
        return budget_breakdown