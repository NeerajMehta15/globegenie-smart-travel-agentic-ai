"""
Input section with quick description and detailed form tabs.
"""
import streamlit as st
from datetime import datetime, timedelta


def render_quick_input_tab():
    """Render quick description input tab"""
    st.markdown("""
    <div class='info-box'>
        💡 <strong>Tip:</strong> Just describe your trip naturally! 
        Example: "5-day romantic getaway to Paris in May, budget $4000, love art and cafes"
    </div>
    """, unsafe_allow_html=True)
    
    user_input_quick = st.text_area(
        "Describe your dream trip:",
        height=150,
        placeholder="Example: I want a 7-day adventure trip to Iceland with my partner. Budget around $6000. "
                    "We love hiking, waterfalls, and northern lights. Traveling in September.",
        help="Include: destination, duration, budget, number of travelers, interests, and travel dates",
        max_chars=1000,
        key="quick_input"
    )
    
    # Character counter
    char_count = len(user_input_quick) if user_input_quick else 0
    st.caption(f"Characters: {char_count}/1000")
    
    return user_input_quick


def render_detailed_form_tab():
    """Render detailed form input tab"""
    st.markdown("Fill in the details below for a structured trip plan:")
    
    with st.form("detailed_trip_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input(
                "🌎 Destination",
                placeholder="e.g., Tokyo, Japan",
                help="Where do you want to go?"
            )
            
            start_date = st.date_input(
                "📅 Start Date",
                value=datetime.now() + timedelta(days=30),
                min_value=datetime.now(),
                max_value=datetime.now() + timedelta(days=365),
                help="When does your trip start?"
            )
            
            duration = st.number_input(
                "⏱️ Duration (days)",
                min_value=1,
                max_value=30,
                value=7,
                step=1,
                help="How many days will you travel?"
            )
            
            travelers = st.number_input(
                "👥 Number of Travelers",
                min_value=1,
                max_value=10,
                value=2,
                step=1
            )
        
        with col2:
            budget = st.slider(
                "💰 Total Budget (USD)",
                min_value=500,
                max_value=20000,
                value=5000,
                step=100,
                format="$%d",
                help="Your total budget for the entire trip"
            )
            
            travel_style = st.selectbox(
                "🎨 Travel Style",
                ["Relaxation & Leisure", "Adventure & Outdoor", "Culture & History", 
                 "Food & Wine", "Luxury", "Budget Backpacking", "Family-Friendly"],
                help="What kind of experience are you looking for?"
            )
            
            accommodation = st.radio(
                "🏨 Accommodation Preference",
                ["Budget (Hostels/Budget Hotels)", "Mid-range (3-star Hotels)", 
                 "Luxury (4-5 star Hotels)"],
                horizontal=False
            )
            
            interests = st.multiselect(
                "❤️ Interests (select multiple)",
                ["Beaches", "Mountains", "Museums", "Hiking", "Nightlife", 
                 "Shopping", "Local Cuisine", "Photography", "Wildlife", 
                 "Historical Sites", "Water Sports", "Wellness & Spa"],
                default=["Local Cuisine"],
                help="What activities interest you most?"
            )
        
        # Additional preferences
        with st.expander("⚙️ Additional Preferences (Optional)"):
            col3, col4 = st.columns(2)
            
            with col3:
                dietary = st.multiselect(
                    "🍽️ Dietary Restrictions",
                    ["None", "Vegetarian", "Vegan", "Halal", "Kosher", 
                     "Gluten-Free", "Allergies"]
                )
                
                transportation = st.multiselect(
                    "🚗 Preferred Transportation",
                    ["Public Transit", "Rental Car", "Taxi/Uber", 
                     "Walking", "Bicycle", "Train"]
                )
            
            with col4:
                pace = st.select_slider(
                    "⚡ Trip Pace",
                    options=["Relaxed", "Moderate", "Fast-paced"],
                    value="Moderate",
                    help="How much do you want to pack into each day?"
                )
                
                flexibility = st.checkbox(
                    "Allow flexible dates (±3 days)",
                    value=False
                )
        
        # Submit button for form
        submitted = st.form_submit_button(
            "🚀 Generate Travel Plan",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Construct detailed prompt from form data
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
            
            # Join all parts into a coherent prompt
            user_input = " ".join(prompt_parts)
            return user_input, True
    
    return "", False


def render_generated_prompt_display():
    """Display the generated prompt from form data"""
    st.markdown("---")
    st.markdown("### 📄 Generated Prompt from Your Form")
    st.markdown("""
    <div class='info-box'>
        ℹ️ <strong>Info:</strong> We've converted your form inputs into a natural language prompt below. 
        This will be sent to the AI for processing.
    </div>
    """, unsafe_allow_html=True)
    
    st.text_area(
        "Generated Prompt:",
        value=st.session_state.generated_prompt,
        height=150,
        disabled=True,
        key="generated_prompt_display"
    )


def render_input_section():
    """
    Render complete input section with tabs.
    Returns: (user_input, generate_clicked)
    """
    st.markdown("### 📝 How would you like to plan your trip?")
    
    input_tab1, input_tab2 = st.tabs(["🚀 Quick Description", "📋 Detailed Form"])
    
    user_input = ""
    generate_clicked = False
    
    with input_tab1:
        user_input_quick = render_quick_input_tab()
        if user_input_quick:
            user_input = user_input_quick
            st.session_state.input_method = "quick"
    
    with input_tab2:
        user_input_detailed, submitted = render_detailed_form_tab()
        if submitted:
            user_input = user_input_detailed
            generate_clicked = True
            st.session_state.input_method = "detailed"
            st.session_state.generated_prompt = user_input_detailed
    
    # Show generated prompt for detailed form
    if st.session_state.input_method == "detailed" and st.session_state.get('generated_prompt'):
        render_generated_prompt_display()
    
    # Generate button for quick input
    if st.session_state.input_method == "quick" and user_input:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Generate Travel Plan", type="primary", use_container_width=True, key="quick_generate"):
                generate_clicked = True
    
    return user_input, generate_clicked