from agent.input_analyzer import InputAnalyzer
from agent.orchestrator import Orchestrator

# Vague input - should trigger FULL research
user_input = "I want a relaxing vacation somewhere warm with beaches, budget around $3000"

print("=== STEP 1: INPUT ANALYSIS ===")
analyzer = InputAnalyzer()
trip_state = analyzer.process_input(user_input)
print(f"Destination: {trip_state.destination}")
print(f"Budget: {trip_state.budget}")
print(f"Duration: {trip_state.duration}")
print(f"Preferences: {trip_state.preferences}")
print()

print("=== STEP 2: ORCHESTRATION ===")
orchestrator = Orchestrator()
final_state = orchestrator.orchestrate_trip_planning(trip_state)
print()

print("=== STEP 3: RESULTS ===")
print(f"Research Status: {final_state.research_status}")

# For full research, check suggested destinations
if 'suggested_destinations' in final_state.destination_research:
    print("\nSUGGESTED DESTINATIONS:")
    for dest in final_state.destination_research['suggested_destinations']:
        print(f"\n- {dest['destination']}")
        print(f"  Why: {dest['why_suitable']}")
        print(f"  Cost: ${dest['estimated_cost']}")
else:
    print(f"\nDestination Research: {final_state.destination_research.get('destination', 'N/A')}")

print(f"\nItinerary Status: {final_state.itinerary_status}")
print(f"Budget Status: {final_state.budget_status}")
print(f"\nFinal Plan Summary: {final_state.final_plan.get('trip_summary', 'No summary')}")