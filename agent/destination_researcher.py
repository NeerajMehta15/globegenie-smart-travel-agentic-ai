from state.trip_state import TripState
from core.llm_client import LLMClient
from core.prompt_library import load_prompt
from typing import Dict, Any

class DestinationResearcher:
    """Agent responsible for researching destinations and providing travel information."""
    
    def __init__(self):
        """Initialize the destination researcher with LLM client."""
        self.llm_client = LLMClient()
    
    def research(self, trip_state: TripState, research_type: str) -> Dict[str, Any]:
        """
        Main method to perform destination research.
        
        Args:
            trip_state: Current trip state with user preferences
            research_type: Either 'light' or 'full'
            
        Returns:
            Dictionary with research results
        """
        # Extract data from trip_state
        destination = trip_state.destination 
        preferences = trip_state.preferences
        trip_type = trip_state.trip_type
        duration = trip_state.duration
        budget = trip_state.budget

        # Loading appropriate prompt
        prompt = self._load_research_prompt(research_type)

        # Format prompt with data
        input_data = {
            'destination': destination,
            'preferences': preferences,
            'trip_type': trip_type,
            'duration': duration,
            'budget': budget
        }
        formatted_prompt = self.llm_client._format_prompt(prompt, input_data)
        # Invoke LLM
        response = self.llm_client.invoke(formatted_prompt)

        # Parse response
        research_data = self.llm_client._parse_json_response(response)
        # Return research dict
        return research_data
    
    
    def _load_research_prompt(self, research_type: str) -> str:
        if research_type == "light":
            prompt = load_prompt('destination_light_research_prompt.txt')
        elif research_type == "full":
            prompt = load_prompt('destination_full_research_prompt.txt')
        else:
            raise ValueError(f"Invalid research_type: {research_type}. Must be 'light' or 'full'")
        return prompt
        
