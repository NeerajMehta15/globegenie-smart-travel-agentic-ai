"""
Helper functions for form handling and validation.
"""
from datetime import datetime


def validate_trip_input(user_input: str) -> tuple:
    """
    Validate user trip input.
    Returns (is_valid, error_message)
    """
    if not user_input or len(user_input.strip()) == 0:
        return False, "⚠️ Please describe your trip first!"
    
    if len(user_input) < 20:
        return False, "⚠️ Please provide more details (at least 20 characters)"
    
    return True, ""


def build_prompt_from_form(destination, start_date, duration, travelers, 
                           budget, travel_style, accommodation, 
                           interests, pace, dietary, transportation, 
                           flexibility) -> str:
    """
    Construct a natural language prompt from form data.
    """
    prompt_parts = []
    prompt_parts.append(f"I want to plan a {duration}-day trip to {destination}.")
    prompt_parts.append(f"Travel dates starting from {start_date.strftime('%B %d, %Y')}.")
    prompt_parts.append(f"Number of travelers: {travelers} {'person' if travelers == 1 else 'people'}.")
    prompt_parts.append(f"Total budget: ${budget}.")
    prompt_parts.append(f"Travel style: {travel_style}.")
    prompt_parts.append(f"Accommodation preference: {accommodation}.")
    
    if interests:
        prompt_parts.append(f"Main interests: {', '.join(interests)}.")
    
    if pace:
        prompt_parts.append(f"Preferred trip pace: {pace}.")
    
    if dietary and "None" not in dietary:
        prompt_parts.append(f"Dietary restrictions: {', '.join(dietary)}.")
    
    if transportation:
        prompt_parts.append(f"Preferred transportation: {', '.join(transportation)}.")
    
    if flexibility:
        prompt_parts.append("Dates are flexible (±3 days).")
    
    return " ".join(prompt_parts)


def format_char_count(current: int, maximum: int) -> str:
    """Format character count display"""
    return f"Characters: {current}/{maximum}"