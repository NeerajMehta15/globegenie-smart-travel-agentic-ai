from agent.input_analyzer import InputAnalyzer
from agent.orchestrator import Orchestrator

# Test input
user_input = "5-day beach vacation to Bali with $4000 budget for 2 people"

# Run workflow
analyzer = InputAnalyzer()
trip_state = analyzer.process_input(user_input)

orchestrator = Orchestrator()
final_state = orchestrator.orchestrate_trip_planning(trip_state)

# Print results
print(final_state.final_plan)