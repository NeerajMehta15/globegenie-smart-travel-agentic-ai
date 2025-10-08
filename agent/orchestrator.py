from state.trip_state import TripState
from agent.destination_researcher import DestinationResearcher
from agent.itinerary_planner import ItineraryPlanner
from agent.budget_analyzer import BudgetAnalyzer
from agent.travel_coordinator import TravelCoordinator
from langgraph.graph import StateGraph, START, END
from core.llm_client import LLMClient
from core.prompt_library import load_prompt


class Orchestrator:
    def __init__(self):
        # Initialize all agents
        self.destination_researcher = DestinationResearcher()
        self.itinerary_planner = ItineraryPlanner()
        self.budget_analyzer = BudgetAnalyzer()
        self.travel_coordinator = TravelCoordinator()
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
            workflow.add_edge('finalization', END)

            
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
        
        prompt_text = load_prompt("destination_evaluation_prompt.txt")

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
        try:
            research_results = self.destination_researcher.research(trip_state, research_type)
            trip_state.destination_research = research_results
            trip_state.research_status = "completed"
            return trip_state
        except Exception as e:
            print(f"Error in destination research: {e}")
            trip_state.research_status = "failed"
            return trip_state
    
    def _execute_parallel_planning(self, trip_state: TripState) -> TripState:
        """Execute itinerary and budget planning in parallel."""
        try:
            #Running itinerary planner
            itinerary = self.itinerary_planner.plan(trip_state)
            if isinstance(itinerary, dict) and 'itinerary' in itinerary:
                trip_state.itinerary_draft = itinerary['itinerary']
            else:
                trip_state.itinerary_draft = itinerary 
            trip_state.itinerary_status = "completed"
            #Running budget analyzer
            budget_analysis = self.budget_analyzer.analyze_budget(trip_state)
            trip_state.budget_breakdown = budget_analysis
            trip_state.budget_status = "completed"
            return trip_state
        except Exception as e:
            print(f"Error in parallel planning: {e}")
            trip_state.itinerary_status = "failed"
            trip_state.budget_status = "failed"
            return trip_state
    
    def _run_optimization_loop(self, trip_state: TripState) -> TripState:
        """Run the budget ↔ itinerary optimization loop."""
        _budget = trip_state.budget
        _itinerary_budget = trip_state.budget_breakdown.get('total_estimated_cost', 0)

        while trip_state.current_loop < trip_state.max_loops:
            if _itinerary_budget <= _budget * 1.05:
                print("Itinerary budget within acceptable range. Optimization complete.")
                trip_state.itinerary_status = "finalized"
                trip_state.budget_status = "finalized"
                trip_state.convergence_score = _budget / _itinerary_budget if _itinerary_budget > 0 else 1.0
                return trip_state

            try:
                print(f"Optimization loop iteration {trip_state.current_loop + 1}: Current cost ${_itinerary_budget}, Target ${_budget}")
                
                optimization_context = {
                    'current_cost': _itinerary_budget,
                    'cost_reduction_needed': _itinerary_budget - _budget
                }
                

                trip_state.itinerary_draft = self.itinerary_planner.plan(trip_state, optimization_context)
                

                trip_state.budget_breakdown = self.budget_analyzer.analyze_budget(trip_state)
                _itinerary_budget = trip_state.budget_breakdown.get('total_estimated_cost', 0)
                

                trip_state.current_loop += 1
                
            except Exception as e:
                print(f"Error during optimization iteration: {e}")
                trip_state.itinerary_status = "optimization_failed"
                trip_state.budget_status = "optimization_failed"
                return trip_state
        

        print(f"Optimization ended after {trip_state.current_loop} iterations. Best effort result.")
        trip_state.itinerary_status = "optimized_partial"
        trip_state.budget_status = "optimized_partial"
        trip_state.convergence_score = _budget / _itinerary_budget if _itinerary_budget > 0 else 1.0
        return trip_state



    def _finalize_travel_plan(self, trip_state: TripState) -> TripState:
        """Create final polished travel plan."""
        try:
            final_plan = self.travel_coordinator.coordinate(trip_state)
            trip_state.final_plan = final_plan
            trip_state.itinerary_status = "finalized"
            trip_state.budget_status = "finalized"
            return trip_state
        except Exception as e:
            print(f"Error in finalizing travel plan: {e}")
            trip_state.itinerary_status = "finalization_failed"
            trip_state.budget_status = "finalization_failed"
            return trip_state
    
    def _handle_user_feedback(self, trip_state: TripState) -> TripState:
        """Process user satisfaction and determine next steps."""
        pass