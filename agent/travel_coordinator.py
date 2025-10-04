from core.llm_client import LLMClient
from core.prompt_library import load_prompt
from state.trip_state import TripState


class TravelCoordinator:
    def __init__(self):
        self.llm_client = LLMClient()
        
    def coordinate(self, trip_state: TripState) -> dict:
        destination = trip_state.destination
        duration = trip_state.duration
        dates = trip_state.dates
        number_of_travelers = trip_state.number_of_travelers
        trip_type = trip_state.trip_type
        destination_research = trip_state.destination_research
        itinerary_draft = trip_state.itinerary_draft
        budget_breakdown = trip_state.budget_breakdown

        # Load travel coordination prompt
        prompt = load_prompt('travel_coordination_prompt.txt')

        #Prepare input data
        input_data = {
            'destination': destination,
            'duration': duration,
            'dates': dates,
            'number_of_travelers': number_of_travelers,
            'trip_type': trip_type,
            'destination_research': destination_research,
            'itinerary_draft': itinerary_draft,
            'budget_breakdown': budget_breakdown
        }

        # Format and invoke LLM
        formatted_prompt = self.llm_client._format_prompt(prompt, input_data)
        try:
            response = self.llm_client.invoke(formatted_prompt)
            final_plan = self.llm_client._parse_json_response(response)
            trip_state.final_plan = final_plan
            return final_plan
        except Exception as e:
                print(f"Error in travel coordination: {e}")
                return {"error": "Failed to generate final travel plan."}