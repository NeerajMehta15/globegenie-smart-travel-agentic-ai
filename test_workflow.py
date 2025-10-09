from agent.input_analyzer import InputAnalyzer
from agent.orchestrator import Orchestrator

user_input = "5-day beach vacation to Bali with $4000 budget for 2 people"

# Step 1: Input Analysis
print("=== STEP 1: INPUT ANALYSIS ===")
analyzer = InputAnalyzer()
trip_state = analyzer.process_input(user_input)
print(f"Destination: {trip_state.destination}")
print(f"Budget: {trip_state.budget}")
print(f"Duration: {trip_state.duration}")
print()

# Step 2: Orchestration
print("=== STEP 2: ORCHESTRATION ===")
orchestrator = Orchestrator()
final_state = orchestrator.orchestrate_trip_planning(trip_state)
print()

# Step 3: Check Each Stage
print("=== STEP 3: RESULTS ===")
print(f"Research Status: {final_state.research_status}")
print(f"Destination Research: {final_state.destination_research}")
print()

print(f"Itinerary Status: {final_state.itinerary_status}")
print(f"Itinerary Draft: {final_state.itinerary_draft}")
print()

print(f"Budget Status: {final_state.budget_status}")
print(f"Budget Breakdown: {final_state.budget_breakdown}")
print()

print(f"Final Plan: {final_state.final_plan}")