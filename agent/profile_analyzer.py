"""
Profile Analyzer Agent

Loads user profiles from the database and generates personalization context
for downstream agents. Handles anonymous users with generic preferences.

Flow:
1. Check if user_id exists
2. Load profile from database (or use generic)
3. Generate personalization context using rule-based logic
4. Return updated state with context
"""

from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.crud import get_user_profile
from db.models import UserProfile
from state.trip_state import TripState


# =================DEFAULT/GENERIC PREFERENCES FOR ANONYMOUS USERS ================= #

GENERIC_PROFILE = {
    "travel_style": "balanced",
    "budget_range": "medium",
    "pace_preference": "moderate",
    "interests": ["general"]
}

# ============================= PROFILE ANALYZER AGENT ============================= #

class ProfileAnalyzer:
    """
    Analyzes user profiles and generates personalization context for trip planning.
    
    Uses rule-based logic to convert user preferences into actionable guidance
    for destination research, itinerary planning, and budget analysis.
    """
    
    def __init__(self):
        """
        Initialize the Profile Analyzer.
        """
        pass

    def analyze(self, state: TripState) -> TripState:
        """
        Analyze user profile and generate personalization context.
        """
        try:
            if state.user_id is None:
                profile = GENERIC_PROFILE.copy()
            else:
                profile = self._load_profile_from_db(state.user_id)
                if profile is None:
                    profile = GENERIC_PROFILE.copy()
            
            context = self._generate_personalization_context(profile)
            state.user_profile = profile
            state.personalization_context = context

            return state
            
        except Exception as e:
            state.user_profile = GENERIC_PROFILE.copy()
            state.personalization_context = self._generate_personalization_context(GENERIC_PROFILE)
            
            return state
    #================================== DATABASE OPERATIONS ===============================#

    def _load_profile_from_db(self, user_id: int) -> Dict:
        """
        Load user profile from the database. If not found, return generic profile.
        """
        db = SessionLocal()
        try:
            profile = get_user_profile(db, user_id)
            if profile is None:
                return GENERIC_PROFILE
            
            profile_dict = self._convert_profile_to_dict(profile)
            return profile_dict
        except Exception as e:
            print(f"Error loading profile for user_id {user_id}: {e}")
            return GENERIC_PROFILE
        finally:
            if db is not None:
                db.close()

    def _convert_profile_to_dict(self, profile: UserProfile) -> Dict:
        """
        Convert UserProfile SQLAlchemy model to dictionary.
        """
        try:
            profile_dict = {
            "travel_style": profile.travel_style,
            "budget_range": profile.budget_range,
            "pace_preference": profile.pace_preference,
            "interests": profile.interests if profile.interests else [],}
            return profile_dict
        except Exception as e:
            print(f"Error converting profile to dict: {e}")
            return GENERIC_PROFILE
    #================================== CONTEXT GENERATION ================================#
    def _generate_personalization_context(self, profile: Dict) -> Dict:
        """
        Generate personalization context from user profile using rule-based analysis.
        """
        context = {}

        # Analyze destination preferences
        context['destination_preferences'] = self._analyze_destination_preferences(profile)
        context['activity_suggestions'] = self._analyze_activity_suggestions(profile)
        context['pace_guidance'] = self._analyze_pace_guidance(profile)
        context['budget_guidance'] = self._analyze_budget_guidance(profile)
        context['user_summary'] = self._generate_user_summary(profile)
        return context
        
    #============================= RULES BASED ANALYSIS METHOD ============================#
    def _analyze_destination_preferences(self, profile: Dict) -> Dict:
        """
        Generate destination preferences based on user profile
        """
        destination_prefs = {}

        # Rule: Travel style influences destination type
        if profile['interest'] == 'beach':
            destination_prefs['type'] = 'coastal, beach destinations'
        elif profile['interest'] == 'relaxed' or profile['interest'] == 'adventure':
            destination_prefs['type'] = 'mountain, nature spots'
        elif profile['interest'] == 'cultural' or profile['interest'] == 'historical':
            destination_prefs['type'] = 'cities with rich history and culture'
        elif profile['interest'] == 'nightlife' or profile['interest'] == 'food':
            destination_prefs['type'] = 'vibrant urban areas with nightlife and culinary scenes'
        else:
            destination_prefs['type'] = 'a mix of popular and unique spots'

        return destination_prefs

    def _analyze_activity_suggestions(self, profile: Dict) -> str:
        """
        Generate activity suggestions from interests and travel style.
        """

        if profile['travel_style'] == 'luxury':
            activities = "leisurely sightseeing, spa days, and casual dining experiences"
        elif profile['travel_style'] == 'adventure':
            activities = "hiking, water sports, and exploring off-the-beaten-path locations"
        elif profile['travel_style'] == 'cultural':
            activities = "museum visits, historical tours, and attending local cultural events"
        else: 
            activities = "a mix of sightseeing, local experiences, and some relaxation time"
        
        return activities
    
    def _analyze_pace_guidance(self, profile: Dict) -> str:
        """
        Determine daily activity count and schedule style from pace preference.
        """
        if profile['pace_preference'] == 'relaxed':
            pace = "1-2 activities per day with plenty of downtime"
        elif profile['pace_preference'] == 'moderate':
            pace = "3-4 activities per day with balanced free time"
        elif profile['pace_preference'] == 'busy':
            pace = "5 or more activities per day with minimal downtime"
        else:
            pace = "a flexible schedule adapting to daily preferences"
        
        return pace
    
    def _analyze_budget_guidance(self, profile: Dict) -> str:
        """
        Generate budget and accommodation guidance from budget range and style
        """
        if profile['budget_range'] == 'low':
            budget = "budget accommodations prefered hostels with range of $15-40 per night, local eateries, and cost-effective activities"
        elif profile['budget_range'] == 'medium':
            budget = "mid-range hotels with budget around $60-120 per night , a mix of local and popular dining options, and a variety of activities"
        elif profile['budget_range'] == 'high':
            budget = "luxury hotels with budget around $150-200 per night, fine dining experiences, and premium activities"
        else:
            budget = "a balanced approach to spending based on daily needs"
        
        return budget

    def _generate_user_summary(self, profile: Dict) -> str:
        """
        Generate a summary of the user's travel preferences.
        """

        summary = (f"User prefers a {profile['travel_style']} travel style, "
                   f"with a {profile['budget_range']} budget range, "
                   f"and a {profile['pace_preference']} pace. "
                   f"Interests include: {', '.join(profile['interests'])}.")
        return summary