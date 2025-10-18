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
            print("=== BUILDING WORKFLOW ===")
            
            # Initialize workflow
            workflow = StateGraph(TripState)
            
            # Add nodes with debug
            print("Adding nodes...")
            workflow.add_node('light_research', self._execute_destination_research_light)
            workflow.add_node('full_research', self._execute_destination_research_full)
            workflow.add_node('parallel_planning', self._execute_parallel_planning)
            workflow.add_node('optimization_loop', self._run_optimization_loop)
            workflow.add_node('finalization', self._finalize_travel_plan)
            
            # Add edges - workflow flow
            print("Adding edges...")
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
            print("Compiling workflow...")
            app = workflow.compile()
            
            # Execute workflow
            print("Executing workflow...")
            print(f"Initial state - Budget: {trip_state.budget}, Destination: {trip_state.destination}")

            
            result = app.invoke(trip_state)
            print("Workflow executed successfully!")

            # Debug: Check what result contains
            print(f"Result type: {type(result)}")

            # LangGraph returns dict with all state fields - convert back to TripState
            if isinstance(result, dict):
                # Create TripState from the dict
                try:
                    final_state = TripState(**result)  # Unpack dict into TripState
                    print(f"Final state - Research: {final_state.research_status}, Itinerary: {final_state.itinerary_status}")
                    return final_state
                except Exception as e:
                    print(f"Error converting result to TripState: {e}")
                    return trip_state

            # If result is already TripState
            if isinstance(result, TripState):
                return result

            # Fallback
            print("WARNING: Unexpected result format")
            return trip_state    
        
        except Exception as e: 
            print(f"Error in workflow orchestration: {e}")
            import traceback
            traceback.print_exc()
            trip_state.research_status = "error"
            return trip_state

    def _execute_destination_research_light(self, trip_state: TripState) -> TripState:
        """Wrapper for light research"""
        print("=== EXECUTING LIGHT RESEARCH ===")
        result = self._execute_destination_research(trip_state, 'light')
        print(f"=== LIGHT RESEARCH COMPLETE - Status: {result.research_status} ===")
        return result

    def _execute_destination_research_full(self, trip_state: TripState) -> TripState:
        """Wrapper for full research"""
        print("=== EXECUTING FULL RESEARCH ===")
        return self._execute_destination_research(trip_state, 'full')
        
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
        print(f">>> _execute_destination_research called with type: {research_type}")
        
        try:
            research_results = self.destination_researcher.research(trip_state, research_type)
            print(f">>> Research results received: {list(research_results.keys()) if research_results else 'EMPTY'}")
            
            # Return NEW state with updates
            return trip_state.model_copy(update={
                'destination_research': research_results,
                'research_status': 'completed'
            })
            
        except Exception as e:
            print(f">>> ERROR: {e}")
            return trip_state.model_copy(update={'research_status': 'failed'})
    
    def _execute_parallel_planning(self, trip_state: TripState) -> TripState:
        try:
            itinerary = self.itinerary_planner.plan(trip_state)
            budget_analysis = self.budget_analyzer.analyze_budget(trip_state)
            
            # Return NEW state
            return trip_state.model_copy(update={
                'itinerary_draft': itinerary,
                'itinerary_status': 'completed',
                'budget_breakdown': budget_analysis,
                'budget_status': 'completed'
            })
            
        except Exception as e:
            print(f"Error in parallel planning: {e}")
            return trip_state.model_copy(update={
                'itinerary_status': 'failed',
                'budget_status': 'failed'
            })
    
    def _run_optimization_loop(self, trip_state: TripState) -> TripState:
        """Run the budget ↔ itinerary optimization loop."""
        _budget = trip_state.budget
        _itinerary_budget = trip_state.budget_breakdown.get('total_estimated_cost', 0)
        current_loop = trip_state.current_loop  # Track locally

        while current_loop < trip_state.max_loops:
            # Check convergence
            if _itinerary_budget <= _budget * 1.05:
                print("Itinerary budget within acceptable range. Optimization complete.")
                return trip_state.model_copy(update={
                    'itinerary_status': 'finalized',
                    'budget_status': 'finalized',
                    'convergence_score': _budget / _itinerary_budget if _itinerary_budget > 0 else 1.0,
                    'current_loop': current_loop
                })
            
            # Not converged - optimize
            try:
                print(f"Optimization loop iteration {current_loop + 1}: Current cost ${_itinerary_budget}, Target ${_budget}")
                
                optimization_context = {
                    'current_cost': _itinerary_budget,
                    'cost_reduction_needed': _itinerary_budget - _budget
                }
                
                # Get new itinerary and budget
                new_itinerary = self.itinerary_planner.plan(trip_state, optimization_context)
                
                # Update trip_state for budget calculation
                temp_state = trip_state.model_copy(update={'itinerary_draft': new_itinerary})
                new_budget = self.budget_analyzer.analyze_budget(temp_state)
                
                # Update for next iteration
                trip_state = trip_state.model_copy(update={
                    'itinerary_draft': new_itinerary,
                    'budget_breakdown': new_budget,
                    'current_loop': current_loop + 1
                })
                
                _itinerary_budget = new_budget.get('total_estimated_cost', 0)
                current_loop += 1
                
            except Exception as e:
                print(f"Error during optimization: {e}")
                return trip_state.model_copy(update={
                    'itinerary_status': 'optimization_failed',
                    'budget_status': 'optimization_failed'
                })
        
        # Max loops reached
        print(f"Optimization ended after {current_loop} iterations. Best effort result.")
        return trip_state.model_copy(update={
            'itinerary_status': 'optimized_partial',
            'budget_status': 'optimized_partial',
            'convergence_score': _budget / _itinerary_budget if _itinerary_budget > 0 else 1.0,
            'current_loop': current_loop
        })



    def _finalize_travel_plan(self, trip_state: TripState) -> TripState:
        """Create final polished travel plan."""
        try:
            final_plan = self.travel_coordinator.coordinate(trip_state)
            
            return trip_state.model_copy(update={
                'final_plan': final_plan
            })
            
        except Exception as e:
            print(f"Error finalizing travel plan: {e}")
            return trip_state.model_copy(update={
                'final_plan': {"error": "Failed to create final plan"}
            })
    
    def _handle_user_feedback(self, trip_state: TripState) -> TripState:
        """Process user satisfaction and determine next steps."""
        pass