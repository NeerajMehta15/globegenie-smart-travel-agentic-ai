from state.trip_state import TripState
from agent.destination_researcher import DestinationResearcher
from agent.itinerary_planner import ItineraryPlanner
from agent.budget_analyzer import BudgetAnalyzer
from agent.travel_coordinator import TravelCoordinator
from agent.feedback_handler import FeedbackHandler
from core.optimization_loop import OptimizationLoop
from langgraph import StateGraph, StateNode, DecisionNode, ParallelNode, START , END
from core.llm_client import LLMClient
from core.prompt_library import load_prompt


class Orchestrator:
    def __init__(self):
        # Initialize all agents
        self.destination_researcher = DestinationResearcher()
        self.itinerary_planner = ItineraryPlanner()
        self.budget_analyzer = BudgetAnalyzer()
        self.travel_coordinator = TravelCoordinator()
        self.feedback_handler = FeedbackHandler()
        self.optimization_loop = OptimizationLoop()
        self.llm_client = LLMClient()
    
    
    def orchestrate_trip_planning(self, trip_state: TripState) -> TripState:
        """Main orchestration method - coordinates the entire workflow."""
        try:
            # Initialize workflow
            workflow = StateGraph(TripState)
            
            # Add nodes
            workflow.add_node('light_research', lambda state: self._execute_destination_research(state, 'light'))
            workflow.add_node('full_research', lambda state: self._execute_destination_research(state, 'full'))
            workflow.add_node('parallel_planning', self._execute_parallel_planning)
            workflow.add_node('optimization_loop', self._run_optimization_loop)
            workflow.add_node('finalization', self._finalize_travel_plan)
            workflow.add_node('feedback_handling', self.feedback_handler)
            
            # Add edges - workflow flow
            workflow.add_conditional_edges(
                START,
                self._evaluate_destination_completeness,
                {
                    'light': 'light_research',
                    'full': 'full_research'
                }
            )
            workflow.add_edge('light_research', 'parallel_planning')
            workflow.add_edge('full_research', 'parallel_planning')
            workflow.add_edge('parallel_planning', 'optimization_loop')
            workflow.add_edge('optimization_loop', 'finalization')
            workflow.add_edge('finalization', 'feedback_handling')
            workflow.add_edge('feedback_handling', END)
            
            # Compile workflow
            app = workflow.compile()
            
            # Execute workflow
            result = app.invoke(trip_state)
            
            print("Workflow executed successfully!")
            return result
            
        except Exception as e:
            print(f"Error in workflow orchestration: {e}")
            trip_state.research_status = "error"
            return trip_state
        
    def _evaluate_destination_completeness(self, trip_state: TripState) -> str:
        """Decision logic: light_research vs full_research vs clarification_needed."""
        destination = trip_state.destination 
        preferences = trip_state.preferences
        
        prompt_text = load_prompt("destination_completeness_evaluation.txt")

        input_data = {'destination': destination, 'preferences': preferences}
        prompt_format = self.llm_client._format_prompt(prompt_text, input_data)

        response = self.llm_client.invoke(prompt_format)
        formatted_response = self.llm_client._parse_json_response(response)

        if formatted_response.get("decision") == "light":
            return "light"
        elif formatted_response.get("decision") == "full":
            return "full"
        else:
            raise ValueError("Invalid decision from destination completeness evaluation.")


    def _execute_destination_research(self, trip_state: TripState, research_type: str) -> TripState:
        """Execute destination research based on type."""
        pass
    
    def _execute_parallel_planning(self, trip_state: TripState) -> TripState:
        """Execute itinerary and budget planning in parallel."""
        pass
    
    def _run_optimization_loop(self, trip_state: TripState) -> TripState:
        """Run the budget ↔ itinerary optimization loop."""
        pass
    
    def _finalize_travel_plan(self, trip_state: TripState) -> TripState:
        """Create final polished travel plan."""
        pass
    
    def _handle_user_feedback(self, trip_state: TripState) -> TripState:
        """Process user satisfaction and determine next steps."""
        pass
    
    def _validate_state(self, trip_state: TripState) -> bool:
        """Validate TripState has required fields for next step."""
        pass
    
    def _update_agent_status(self, trip_state: TripState, agent_name: str, status: str) -> TripState:
        """Update agent progress status in TripState."""
        pass
    
    def _check_early_termination(self, trip_state: TripState) -> bool:
        """Check if workflow should terminate early (errors, impossible constraints)."""
        pass