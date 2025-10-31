"""
Application constants and configuration values.
"""

# Budget limits
MIN_BUDGET = 500
MAX_BUDGET = 20000
DEFAULT_BUDGET = 5000

# Trip duration
MIN_DURATION = 1
MAX_DURATION = 30
DEFAULT_DURATION = 7

# Travelers
MIN_TRAVELERS = 1
MAX_TRAVELERS = 10
DEFAULT_TRAVELERS = 2

# Text limits
MAX_INPUT_CHARS = 1000

# Travel styles
TRAVEL_STYLES = [
    "Relaxation & Leisure",
    "Adventure & Outdoor",
    "Culture & History",
    "Food & Wine",
    "Luxury",
    "Budget Backpacking",
    "Family-Friendly"
]

# Accommodation types
ACCOMMODATION_TYPES = [
    "Budget (Hostels/Budget Hotels)",
    "Mid-range (3-star Hotels)",
    "Luxury (4-5 star Hotels)"
]

# Interests options
INTERESTS_OPTIONS = [
    "Beaches", "Mountains", "Museums", "Hiking",
    "Nightlife", "Shopping", "Local Cuisine",
    "Photography", "Wildlife", "Historical Sites",
    "Water Sports", "Wellness & Spa"
]

# Dietary restrictions
DIETARY_OPTIONS = [
    "None", "Vegetarian", "Vegan", "Halal",
    "Kosher", "Gluten-Free", "Allergies"
]

# Transportation options
TRANSPORTATION_OPTIONS = [
    "Public Transit", "Rental Car", "Taxi/Uber",
    "Walking", "Bicycle", "Train"
]

# Pace options
PACE_OPTIONS = ["Relaxed", "Moderate", "Fast-paced"]