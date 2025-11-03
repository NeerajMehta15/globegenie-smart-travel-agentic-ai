from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from utils.config import config
from state.trip_state import TripState
import json


class InputAnalyzer: 
    def __init__(self, user_input: str = None):
        self.user_input = user_input
        self.prompt_template = None
        

    def analyze_input(self):
        '''Analyze user input to extract structured trip details.'''
        self.prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an intelligent travel assistant. 
    Your job is to carefully analyze a user's trip request and extract structured trip details. 
    If any detail is not explicitly mentioned, use defaults or make a reasonable inference from the context.

    ### Fields to extract:
    - destination: str  
    - Extract the city/country/region if mentioned.
    - If vague like "somewhere warm", map to a reasonable placeholder (e.g., "Tropical destination").
    - Default = "Not specified".

    - duration: int (days)  
    - Look for keywords like "weekend", "2 weeks", "next 5 days".
    - If not defined, default = 7.

    - budget: float (USD)  
    - If the user says "budget trip" → 1000.
    - If "luxury trip" or "no budget constraint" → 5000.
    - If user mentions in INR/Euros, convert approx to USD.
    - Default = 1000.

    - dates: dict {{"start_date": str, "end_date": str}}  
    - Extract exact dates if given.
    - If user says "next month", resolve relative time.
    - Default = today's date as start_date, plus duration as end_date.

    - number_of_travelers: int  
    - Detect from mentions like "me and my wife", "group of 4 friends".
    - Default = 2.

    - trip_type: Literal["leisure", "business", "adventure", "cultural", "family", "romantic"]  
    - Infer from intent:  
        - "honeymoon" : romantic  
        - "conference" : business  
        - "backpacking" : adventure  
        - "temples/museums" : cultural  
        - "with kids/parents" : family  
        - If not clear : leisure.

    - preferences: list[Literal["mountains", "beach", "city", "nature", "historical"]]  
    - Extract likes/dislikes.
    - If user says "relax by the ocean" : beach, "hike Himalayas" : mountains, "explore old forts" : historical.
    - Can have multiple values.
    - Default = [].

    ### Output:
    Return the extracted information in **strict JSON format**:
    {{
    "destination": "...",
    "duration": ...,
    "budget": ...,
    "dates": {{"start_date": "...", "end_date": "..."}},
    "number_of_travelers": ...,
    "trip_type": "...",
    "preferences": ["..."]
    }}"""
            ),
            (
                "user",
                "Analyze this user input and extract trip details: {user_input}"
            ),
        ])
        return self.prompt_template
    
    def parse_response(self) -> str: 
        '''Parse the LLM response to extract structured trip details.'''
        try:
            formatted_prompt = self.prompt_template.format_messages(user_input=self.user_input)
            llm = ChatGroq(
                groq_api_key=config.GROQ_API_KEY,
                model="llama-3.1-8b-instant",
                temperature=0.1,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
            response = llm.invoke(formatted_prompt)
            
            return response.content.strip()
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            return "" 

    def _parse_json_response(self, response_content: str) -> dict:
        """Simple JSON parser for LLM responses."""
        import re
        
        try:
            # Remove markdown code blocks if present
            cleaned = response_content.strip()
            if '```json' in cleaned:
                # Extract content between ```json and ```
                start = cleaned.find('```json') + 7
                end = cleaned.find('```', start)
                cleaned = cleaned[start:end].strip()
            
            # Remove single-line // comments (they break JSON)
            cleaned = re.sub(r'//.*', '', cleaned)
            
            # Parse JSON
            return json.loads(cleaned)
            
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Content was: {response_content[:200]}...")
            return {}

    def save_to_state(self, extracted_data: dict) -> TripState:
        """Creating TripState instance from extracted data"""
        try:
            trip_state = TripState(
                # User input section
                raw_input=self.user_input,
                parsed_input=extracted_data,
                
                # Trip details from extracted data
                destination=extracted_data.get('destination', 'Not specified'),
                duration=extracted_data.get('duration', 7),
                budget=extracted_data.get('budget', 1000.0),
                dates=extracted_data.get('dates', {}),
                
                number_of_travelers=extracted_data.get('number_of_travelers', 2),  # Was: [2]
                
                trip_type=extracted_data.get('trip_type', 'leisure'), 
                
                preferences=extracted_data.get('preferences', ['city']),
                
                # Agent progress - initialize as pending
                research_status="pending",
                itinerary_status="pending", 
                budget_status="pending",
                
                # Loop management - initialize
                current_loop=0,
                max_loops=2,  # default
                convergence_score=0.0,
                
                # Results - initialize as empty
                destination_research={},
                itinerary_draft= {},
                budget_breakdown={},
                final_plan={},
                
                # User feedback - initialize
                user_satisfaction="neutral",
                feedback_notes=""

                #User profile and personalization context
                user_id=None,  
                user_profile=None, 
                personalization_context=None
            )
            return trip_state
            
        except Exception as e:
            print(f"Error creating TripState: {e}")

            return TripState(
                raw_input=self.user_input,
                parsed_input={},
                destination="Not specified",
                duration=7,
                budget=1000.0,
                dates={},
                number_of_travelers=2, 
                trip_type="leisure",
                preferences=["city"],
                research_status="pending",
                itinerary_status="pending",
                budget_status="pending",
                current_loop=0,
                max_loops=5,
                convergence_score=0.0,
                destination_research={},
                itinerary_draft={},
                budget_breakdown={},
                final_plan={},
                user_satisfaction="neutral",
                feedback_notes="",
                user_id="",  
                user_profile={}, 
                personalization_context={}
            )

    def process_input(self, user_input: str = None) -> TripState:  
        '''Main method to process user input and return TripState.'''
        
        if user_input is not None:
            self.user_input = user_input

        prompt_template = self.analyze_input() 
        response_content = self.parse_response()
        extracted_data = self._parse_json_response(response_content)
        trip_state = self.save_to_state(extracted_data)
        return trip_state