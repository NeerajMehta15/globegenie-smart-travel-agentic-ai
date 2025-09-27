 #3. Recommendation Agent
recommendation_template = ChatPromptTemplate.from_messages([
    ("system", """You are a Travel Recommendation Specialist. Your job is to:
    1. Enhance an existing travel itinerary with personalized recommendations
    2. Suggest specific restaurants, attractions, and activities based on user interests
    3. Add local insights that match the user's preferences
    4. Ensure all recommendations maintain budget constraints

    You will receive an itinerary and should return an ENHANCED version of that itinerary
    with the same JSON structure but with added or improved activities and details.

    The JSON structure should have these keys:
    - destination: string
    - days: array of day objects, each containing:
      - date: string in YYYY-MM-DD format
      - activities: array of activity objects, each containing:
        - name: string
        - description: string
        - location: string
        - duration_hours: number
        - cost: number
        - category: string
        - suitable_for_interests: array of strings
      - accommodation: string
      - total_day_cost: number
      - transportation: array of strings
    - total_cost: number
    - remaining_budget: number

    Return ONLY valid JSON without any other text or explanation.
    """),
    ("human", """
    Enhance this travel itinerary with personalized recommendations:
    {itinerary_json}

    User constraints and preferences:
    {constraints_json}

    Focus on providing specific, personalized recommendations that match their interests.
    """),
])

def recommendation_node():
    def enhance_with_recommendations(state: Dict[str, Any]) -> Dict[str, Any]:
        constraints = state.get("constraints", {})
        itinerary = state.get("itinerary", {})

        try:
            # Convert to JSON strings for the prompt
            constraints_json = json.dumps(constraints)
            itinerary_json = json.dumps(itinerary)

            # Get enhanced recommendations
            response = llm.invoke(recommendation_template.format_messages(constraints_json=constraints_json,itinerary_json=itinerary_json))

            enhanced_itinerary = parse_json_from_llm(response.content)
            return {"enhanced_itinerary": enhanced_itinerary, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    return enhance_with_recommendations
