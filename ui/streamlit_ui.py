import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adjust the path to include the parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from agent.input_analyzer import InputAnalyzer
from agent.orchestrator import Orchestrator

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="GlobeGenie - AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/globegenie',
        'Report a bug': "https://github.com/yourusername/globegenie/issues",
        'About': """
        # GlobeGenie 🌍
        ### Your AI Travel Planning Assistant
        
        Version 1.0.0
        
        Plan your dream vacation with AI-powered personalized itineraries, 
        budget optimization, and destination insights.
        """
    }
)

# ==================== CUSTOM CSS STYLING - ANTHROPIC THEME ====================
st.markdown("""
 <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - Soft Ivory Background */
    .main {
        background-color: #FAF9F6;
        color: #1C1917;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #1C1917;
        font-weight: 700;
        padding-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #292524;
        font-weight: 600;
        padding-top: 1rem;
    }
    
    h3 {
        color: #292524;
        font-weight: 500;
    }
    
    /* Gradient Header Box */
    .gradient-header {
        background: linear-gradient(135deg, #D97757 0%, #C8613D 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(217, 119, 87, 0.3);
    }
    
    .gradient-header h3 {
        color: white;
        margin: 0 0 0.5rem 0;
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    .gradient-header p {
        margin: 0;
        opacity: 0.95;
        font-size: 1.05rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E7E5E4;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: #FFF7F3;
        border-color: #D97757;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(217, 119, 87, 0.2);
    }
    
    .feature-card h3 {
        color: #1C1917;
        margin-top: 0;
        font-size: 1.1rem;
    }
    
    .feature-card p {
        color: #44403C;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Button Styling */
    .stButton>button {
        /* CHANGED: Replaced red with orange gradient */
        background: linear-gradient(135deg, #D97757 0%, #C8613D 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(217, 119, 87, 0.3);
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        /* CHANGED: Replaced red hover with orange hover gradient */
        background: linear-gradient(135deg, #E88668 0%, #D97757 100%);
        box-shadow: 0 6px 20px rgba(217, 119, 87, 0.5);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        background-color: #FFFFFF;
        border: 2px solid #E7E5E4;
        border-radius: 8px;
        color: #1C1917;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #D97757;
        box-shadow: 0 0 0 3px rgba(217, 119, 87, 0.1);
        background-color: #FFF7F3;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #A8A29E;
    }
    
    /* Labels */
    .stTextInput>label,
    .stTextArea>label,
    .stSelectbox>label,
    .stNumberInput>label,
    .stSlider>label,
    .stRadio>label,
    .stMultiselect>label,
    .stDateInput>label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        /* CHANGED: Replaced red with orange for slider fill */
        background-color: #D97757; 
    }
    
    .stSlider>div>div>div {
        background-color: #E7E5E4;
    }
    
    /* Radio Buttons */
    .stRadio>div {
        background-color: transparent;
    }
    
    .stRadio>div>label>div {
        background-color: #FFFFFF;
        border: 2px solid #E7E5E4;
        color: #1C1917;
    }
    
    .stRadio>div>label>div:hover {
        border-color: #D97757;
        background-color: #FFF7F3;
    }
    
    /* Multiselect */
    .stMultiselect>div>div>div {
        background-color: #FFFFFF;
        border: 2px solid #E7E5E4;
    }
    
    .stMultiselect span {
        color: #1C1917;
    }

    /* Custom style for tags like "Local Cuisine", "Hiking" */
    /* You might need to inspect the Streamlit HTML to target these precisely.
       This is a generic class for demonstration. */
    .st-chip-accent { /* This class would need to be applied manually or targeted more specifically */
        background-color: #D97757 !important; /* Orange background */
        color: white !important; /* White text for contrast */
        border-color: #D97757 !important; /* Orange border */
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #D97757;
    }
    
    [data-testid="stMetricLabel"] {
        color: #44403C;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #15803D;
    }
    
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E7E5E4;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-radius: 8px;
        color: #44403C;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FFF7F3;
        color: #1C1917;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #D97757 0%, #C8613D 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-radius: 8px;
        color: #1C1917;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #FFF7F3;
        border-color: #D97757;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Alert Boxes */
    .stAlert {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-radius: 8px;
        color: #1C1917;
    }
    
    div[data-baseweb="notification"] {
        background-color: #FFFFFF;
        border-left-width: 4px;
    }
    
    /* Success */
    .stSuccess {
        background-color: rgba(21, 128, 61, 0.1);
        border-left-color: #15803D;
    }
    
    /* Info */
    .stInfo {
        /* CHANGED: Replaced red info accent with orange */
        background-color: rgba(217, 119, 87, 0.1);
        border-left-color: #D97757;
    }
    
    /* Warning */
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
    }
    
    /* Error */
    .stError {
        /* CHANGED: Replaced red error accent with orange (though typically error is red) */
        background-color: rgba(217, 119, 87, 0.1); /* Using the primary accent orange */
        border-left-color: #D97757; /* Using the primary accent orange */
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FAF9F6 100%);
        border-right: 1px solid #E7E5E4;
    }
    
    [data-testid="stSidebar"] * {
        color: #1C1917;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1C1917;
    }
    
    /* Progress Bar */
    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #D97757 0%, #C8613D 100%);
    }
    
    .stProgress>div>div>div {
        background-color: #E7E5E4;
    }
    
    /* Spinner */
    .stSpinner>div {
        border-top-color: #D97757;
    }
    
    /* Custom Info Box */
    .info-box {
        background-color: rgba(217, 119, 87, 0.15) !important;
        border-left: 4px solid #D97757 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
        color: #FFD6B0 !important;        /* Strong orange for text */
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(217,119,87,0.08) !important;
    }
            
    .info-box strong {
        color: #FFD6B0 !important; 
        font-weight: 700 !important;
    }
    
    /* Divider */
    hr {
        border-color: #E7E5E4;
    }
    
    /* Download Button */
    .stDownloadButton>button {
        background-color: #FFFFFF;
        border: 2px solid #E7E5E4;
        color: #1C1917;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background-color: #FFF7F3;
        border-color: #D97757;
    }
    
    /* Form */
    .stForm {
        background-color: transparent;
        border: none;
    }
    
    /* Checkbox */
    .stCheckbox>label>span {
        color: #292524;
    }
    
    /* Date Input */
    .stDateInput>div>div>input {
        background-color: #FFFFFF;
        border: 2px solid #E7E5E4;
        color: #1C1917;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F4;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D6D3D1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #A8A29E;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E7E5E4;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'final_state' not in st.session_state:
    st.session_state.final_state = None
if 'plan_history' not in st.session_state:
    st.session_state.plan_history = []
if 'input_method' not in st.session_state:
    st.session_state.input_method = "quick"
if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&q=80", 
             use_container_width=True)
    
    st.title("🌍 GlobeGenie")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to GlobeGenie! ✈️
    
    Your AI-powered travel companion that creates personalized 
    itineraries based on your preferences, budget, and travel style.
    
    #### How it works:
    1. 📝 Describe your dream trip
    2. 🤖 AI analyzes and plans
    3. 📋 Get detailed itinerary
    4. 💾 Download or modify
    """)
    
    st.markdown("---")
    
    # API Key Input - DISABLED FOR NOW
    groq_api_key = "demo_mode"  # Dummy value to bypass API key checks
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("#### 📊 Your Stats")
    col1, col2 = st.columns(2)
    col1.metric("Plans Created", len(st.session_state.plan_history))
    col2.metric("Destinations", "0")
    
    st.markdown("---")
    
    # Help Section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        **Tips for better results:**
        - Be specific about destinations
        - Mention your travel dates
        - Include budget constraints
        - State your preferences clearly
        
        **Example:**
        "7-day trip to Japan in April, budget $5000 
        for 2 people, interested in culture and food"
        """)

# ==================== MAIN HEADER ====================
st.title("🌍 GlobeGenie - AI Travel Planner")

# Custom Gradient Header
st.markdown("""
<div class='gradient-header'>
    <h3>Plan Your Perfect Journey with AI</h3>
    <p>From budget backpacking to luxury escapes - personalized itineraries in seconds</p>
</div>
""", unsafe_allow_html=True)

# ==================== FEATURE HIGHLIGHTS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>🎯 Personalized</h3>
        <p>Tailored to your preferences and budget</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>⚡ Fast</h3>
        <p>Complete itinerary in under 60 seconds</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <h3>💰 Smart Budget</h3>
        <p>Optimized costs with detailed breakdown</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='feature-card'>
        <h3>🗺️ Local Insights</h3>
        <p>Hidden gems and authentic experiences</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== INPUT METHOD SELECTOR ====================
st.markdown("### 📝 How would you like to plan your trip?")

input_tab1, input_tab2 = st.tabs(["🚀 Quick Description", "📋 Detailed Form"])

# Variable to hold the final prompt
user_input = ""

with input_tab1:
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
    
    if user_input_quick:
        user_input = user_input_quick
        st.session_state.input_method = "quick"

with input_tab2:
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
            width="stretch"
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
            st.session_state.generated_prompt = user_input
            st.session_state.input_method = "detailed"

# ==================== GENERATE BUTTON (for quick input) ====================
if st.session_state.input_method == "quick" and user_input_quick:
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        generate_button = st.button(
            "🚀 Generate Travel Plan",
            type="primary",
            width="stretch",
            key="quick_generate"
        )
else:
    generate_button = submitted if st.session_state.input_method == "detailed" else False

# ==================== SHOW GENERATED PROMPT (for detailed form) ====================
if st.session_state.input_method == "detailed" and st.session_state.generated_prompt:
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

# ==================== PROCESSING LOGIC ====================
if generate_button:
    if not user_input or len(user_input.strip()) == 0:
        st.warning("⚠️ Please describe your trip first!")
    else:
        # Validation passed - show processing
        st.markdown("---")
        
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            st.markdown("""
            <div style='background-color: rgba(217, 119, 87, 0.1); padding: 1.5rem; 
                        border-radius: 12px; border-left: 4px solid #D97757;'>
                <h4 style='margin-top: 0; color: #C8613D;'>
                    ✨ Creating Your Perfect Itinerary
                </h4>
                <p style='margin-bottom: 0; color: #FFFFFF;'>
                    This may take 30-60 seconds. We're analyzing destinations, 
                    optimizing costs, and crafting personalized recommendations...
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulated multi-step process
            steps = [
                ("Analyzing your preferences...", 20),
                ("Researching destination options...", 40),
                ("Finding best attractions and activities...", 60),
                ("Optimizing daily itinerary...", 80),
                ("Calculating detailed budget...", 90),
                ("Finalizing your travel plan...", 100)
            ]
            
            import time
            for step_text, progress_value in steps:
                status_text.markdown(f"**{step_text}**")
                progress_bar.progress(progress_value)
                time.sleep(0.5)
            
            # Actual workflow execution
            try:
                analyzer = InputAnalyzer()
                trip_state = analyzer.process_input(user_input)
                
                orchestrator = Orchestrator()
                final_state = orchestrator.orchestrate_trip_planning(trip_state)
                
                st.session_state.final_state = final_state
                st.session_state.show_results = True
                st.session_state.plan_history.append({
                    'date': datetime.now(),
                    'input': user_input[:100] + '...',
                    'state': final_state
                })
                
            except Exception as e:
                st.error(f"❌ Error generating plan: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                st.session_state.show_results = False
            
            # Clear progress indicators
            status_text.empty()
            progress_bar.empty()
            
            if st.session_state.show_results:
                st.balloons()
                st.success("✅ Your personalized travel plan is ready!")

# ==================== RESULTS DISPLAY ====================
if st.session_state.get('show_results', False) and st.session_state.final_state:
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Success header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #15803D 0%, #14532D 100%); 
                padding: 1.5rem; border-radius: 12px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>🎉 Your Travel Plan is Ready!</h2>
        <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.95;'>
            Scroll down to explore your personalized itinerary
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    final_state = st.session_state.final_state
    
    # Quick Actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            "📥 Download PDF",
            data="Sample PDF content",
            file_name="my_trip_plan.pdf",
            mime="application/pdf",
            width="stretch"
        )
    
    with col2:
        st.button("📧 Email Plan", width="stretch")
    
    with col3:
        st.button("🔄 Modify Plan", width="stretch")
    
    with col4:
        if st.button("🗑️ Clear Results", width="stretch"):
            st.session_state.show_results = False
            st.session_state.generated_prompt = ""
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("### 📊 Trip Summary at a Glance")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    # Access final_plan correctly as attribute
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    budget_summary = final_plan.get('budget_summary', {}) if isinstance(final_plan, dict) else {}
    
    with metric_col1:
        st.metric(
            label="Total Cost",
            value=f"${budget_summary.get('total_cost', 0)}",
            delta=f"-${budget_summary.get('savings', 0)}",
            delta_color="inverse"
        )
    
    with metric_col2:
        itinerary = final_plan.get('itinerary', []) if isinstance(final_plan, dict) else []
        itinerary_days = len(itinerary)
        st.metric(
            label="Duration",
            value=f"{itinerary_days} days" if itinerary_days > 0 else "TBD",
            delta="Perfect length"
        )
    
    with metric_col3:
        st.metric(
            label="Per Person",
            value=f"${budget_summary.get('per_person', 0)}",
            delta="Within budget"
        )
    
    with metric_col4:
        # Count activities
        total_activities = 0
        if isinstance(itinerary, list):
            for day in itinerary:
                if isinstance(day, dict):
                    activities = day.get('activities', [])
                    if isinstance(activities, list):
                        total_activities += len(activities)
        
        st.metric(
            label="Activities",
            value=total_activities,
            delta="Planned"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabbed Results
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", 
        "🗓️ Day-by-Day Itinerary", 
        "💰 Budget Breakdown", 
        "✈️ Travel Essentials",
        "🎒 Packing List"
    ])
    
    # TAB 1: Overview
    with tab1:
        st.markdown("### 🌟 Your Trip Overview")
        
        trip_summary = final_plan.get('trip_summary', 
            "Experience the perfect blend of adventure and relaxation on this carefully curated journey.")
        
        st.markdown(f"""
        <div style='background-color: #FFFFFF; padding: 1.5rem; 
                    border-radius: 8px; border-left: 4px solid #D97757; border: 1px solid #E7E5E4;'>
            <p style='font-size: 1.1rem; line-height: 1.7; margin: 0; color: #1C1917;'>
                {trip_summary}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Destination Research
        dest_research = final_state.destination_research if hasattr(final_state, 'destination_research') else {}
        
        if dest_research:
            st.markdown("### 🗺️ Suggested Destinations")
            
            suggested_destinations = dest_research.get('suggested_destinations', [])
            
            if suggested_destinations:
                for i, dest in enumerate(suggested_destinations, 1):
                    if isinstance(dest, dict):
                        dest_name = dest.get('destination', f'Destination {i}')
                        dest_why = dest.get('why_suitable', '')
                        dest_attractions = dest.get('attractions', [])
                        dest_cost = dest.get('estimated_cost', 0)
                        
                        st.markdown(f"""
                        <div style='background-color: #FFFFFF; padding: 1.5rem; 
                                    margin-bottom: 1rem; border-radius: 8px; 
                                    border-left: 3px solid #D97757; border: 1px solid #E7E5E4;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #C8613D;'>
                                {i}. {dest_name}
                            </h4>
                            <p style='margin: 0.5rem 0; color: #1C1917;'>
                                {dest_why}
                            </p>
                            <p style='margin: 0.5rem 0 0 0; color: #44403C;'>
                                <strong>Top Attractions:</strong> {', '.join(dest_attractions) if dest_attractions else 'Various activities'}
                            </p>
                            <p style='margin: 0.5rem 0 0 0; color: #15803D; font-weight: 600;'>
                                Estimated Cost: ${dest_cost}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Destination suggestions will be available soon")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # TAB 2: Itinerary
    with tab2:
        st.markdown("### 📅 Your Day-by-Day Adventure")
        
        itinerary = final_plan.get('itinerary', []) if isinstance(final_plan, dict) else []
        
        if not itinerary:
            st.info("No itinerary data available yet. The AI is still processing your request.")
        else:
            for idx, day_plan in enumerate(itinerary, start=1):
                if not isinstance(day_plan, dict):
                    continue
                
                day_number = day_plan.get('day', idx)
                day_theme = day_plan.get('theme', 'Activities')
                day_cost = day_plan.get('total_day_cost', 0)
                
                with st.expander(
                    f"**Day {day_number}:** {day_theme} (${day_cost})",
                    expanded=(day_number == 1)
                ):
                    activities = day_plan.get('activities', [])
                    
                    if not activities:
                        st.info("No activities planned for this day yet.")
                    else:
                        for activity in activities:
                            if not isinstance(activity, dict):
                                continue
                            
                            activity_time = activity.get('time', 'TBD')
                            activity_name = activity.get('activity', 'Activity')
                            activity_location = activity.get('location', 'Location TBD')
                            activity_duration = activity.get('duration', 'TBD')
                            activity_cost = activity.get('estimated_cost', 0)
                            activity_notes = activity.get('notes', '')
                            
                            st.markdown(f"""
                            <div style='background-color: #FFFFFF; padding: 1rem; 
                                        margin-bottom: 1rem; border-radius: 8px; 
                                        border-left: 3px solid #D97757; border: 1px solid #E7E5E4;'>
                                <h4 style='margin: 0 0 0.5rem 0; color: #C8613D;'>
                                    ⏰ {activity_time} - {activity_name}
                                </h4>
                                <p style='margin: 0.25rem 0; color: #1C1917;'>
                                    <strong>📍 Location:</strong> {activity_location}<br>
                                    <strong>⏱️ Duration:</strong> {activity_duration}<br>
                                    <strong>💵 Cost:</strong> ${activity_cost}
                                </p>
                                {f"<p style='margin: 0.5rem 0 0 0; font-style: italic; color: #44403C;'>💡 {activity_notes}</p>" if activity_notes else ''}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style='text-align: right; font-weight: 600; color: #15803D; 
                                padding-top: 0.5rem; border-top: 2px solid #E7E5E4;'>
                        Total Day Cost: ${day_cost}
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 3: Budget
    with tab3:
        st.markdown("### 💰 Complete Budget Analysis")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Budget", f"${budget_summary.get('total_cost', 0)}")
        
        with col2:
            st.metric("Per Person", f"${budget_summary.get('per_person', 0)}")
        
        with col3:
            total_cost = budget_summary.get('total_cost', 0)
            num_days = len(itinerary)
            daily_avg = total_cost // num_days if num_days > 0 else 0
            st.metric("Daily Average", f"${daily_avg}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Budget breakdown
        breakdown = budget_summary.get('breakdown', {})
        
        if breakdown:
            st.markdown("#### 📊 Cost by Category")
            
            # Create visual breakdown
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Simple bar chart visualization
                import pandas as pd
                
                chart_data = pd.DataFrame({
                    'Category': [cat.replace('_', ' ').title() for cat in breakdown.keys()],
                    'Amount': list(breakdown.values())
                })
                
                st.bar_chart(chart_data, x='Category', y='Amount', height=300)
            
            with col2:
                st.markdown("**Detailed Breakdown:**")
                
                total = sum(breakdown.values())
                
                for category, amount in breakdown.items():
                    percentage = (amount / total) * 100 if total > 0 else 0
                    st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <strong style='color: #1C1917;'>{category.replace('_', ' ').title()}</strong><br>
                        <span style='font-size: 1.2rem; color: #D97757;'>${amount}</span>
                        <span style='color: #44403C;'> ({percentage:.1f}%)</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Budget breakdown will be available once the itinerary is complete.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Money-saving tips
        st.markdown("#### 💡 Money-Saving Tips")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
            **Before You Go:**
            - ✓ Book flights 6-8 weeks in advance
            - ✓ Use price comparison tools
            - ✓ Consider shoulder season travel
            - ✓ Look for package deals
            """)
        
        with tips_col2:
            st.markdown("""
            **During Your Trip:**
            - ✓ Use public transportation
            - ✓ Eat at local restaurants
            - ✓ Book activities online in advance
            - ✓ Use city tourist cards
            """)
    
    # TAB 4: Travel Essentials
    with tab4:
        st.markdown("### ✈️ Essential Travel Information")
        
        essentials = final_plan.get('travel_essentials', {}) if isinstance(final_plan, dict) else {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Documentation")
            st.markdown(f"""
            **Visa Requirements:**  
            {essentials.get('visa', 'Check with embassy')}
            
            **Travel Insurance:**  
            {essentials.get('insurance', 'Recommended')}
            
            **Required Documents:**
            - Valid passport (6 months validity)
            - Return flight tickets
            - Hotel reservations
            - Travel insurance proof
            """)
            
            st.markdown("#### 💱 Money Matters")
            st.markdown(f"""
            **Currency:**  
            {essentials.get('currency', 'Local currency info')}
            
            **Payment Methods:**
            - Credit cards widely accepted
            - ATMs available throughout
            - Carry some cash for small vendors
            - Notify bank before traveling
            """)
        
        with col2:
            st.markdown("#### 🌡️ Weather & Climate")
            st.markdown(f"""
            **Expected Conditions:**  
            {essentials.get('weather', 'Check local forecast')}
            
            **What to Pack:**
            - Light layers for day
            - Warmer jacket for evenings
            - Comfortable walking shoes
            - Rain jacket (just in case)
            """)
            
            st.markdown("#### 🗣️ Communication")
            st.markdown(f"""
            **Language:**  
            {essentials.get('language', 'Local language info')}
            
            **Time Zone:**  
            {essentials.get('timezone', 'Local timezone')}
            
            **Useful Phrases:**
            - Hello / Thank you / Please
            - Download translation app
            - Learn basic numbers
            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Health & Safety
        st.markdown("#### 🏥 Health & Safety")
        
        safety_col1, safety_col2 = st.columns(2)
        
        with safety_col1:
            st.markdown("""
            **Health Precautions:**
            - Check vaccination requirements
            - Pack basic first-aid kit
            - Bring prescription medications
            - Know emergency numbers (112)
            """)
        
        with safety_col2:
            st.markdown("""
            **Safety Tips:**
            - Register with embassy
            - Keep copies of documents
            - Be aware of surroundings
            - Use licensed taxis/rideshares
            """)
    
    # TAB 5: Packing List
    with tab5:
        st.markdown("### 🎒 Smart Packing Checklist")
        
        packing_list = final_plan.get('packing_list', []) if isinstance(final_plan, dict) else []
        
        if not packing_list:
            st.info("Packing list will be generated based on your destination and activities.")
        else:
            # Check if packing_list is a dictionary or list
            if isinstance(packing_list, dict):
                # Dictionary format
                pack_col1, pack_col2 = st.columns(2)
                
                categories = list(packing_list.keys())
                mid_point = len(categories) // 2
                
                with pack_col1:
                    for category in categories[:mid_point + 1]:
                        st.markdown(f"#### {category}")
                        items = packing_list.get(category, [])
                        for i, item in enumerate(items):
                            st.checkbox(str(item), key=f"pack_{category}_{i}")
                        st.markdown("<br>", unsafe_allow_html=True)
                
                with pack_col2:
                    for category in categories[mid_point + 1:]:
                        st.markdown(f"#### {category}")
                        items = packing_list.get(category, [])
                        for i, item in enumerate(items):
                            st.checkbox(str(item), key=f"pack_{category}_{i}")
                        st.markdown("<br>", unsafe_allow_html=True)
                        
            elif isinstance(packing_list, list):
                # List format
                st.markdown("#### Essential Items to Pack")
                
                pack_col1, pack_col2 = st.columns(2)
                mid_point = len(packing_list) // 2
                
                with pack_col1:
                    for i, item in enumerate(packing_list[:mid_point]):
                        st.checkbox(str(item), key=f"pack_item_{i}")
                
                with pack_col2:
                    for i, item in enumerate(packing_list[mid_point:], start=mid_point):
                        st.checkbox(str(item), key=f"pack_item_{i}")
            else:
                st.warning(f"Packing list format not recognized. Type: {type(packing_list)}")
        
        # Packing tips
        st.markdown("---")
        st.markdown("#### 💡 Pro Packing Tips")
        
        tips_col1, tips_col2, tips_col3 = st.columns(3)
        
        with tips_col1:
            st.markdown("""
            **Space Savers:**
            - Roll clothes instead of folding
            - Use packing cubes
            - Wear bulky items on plane
            """)
        
        with tips_col2:
            st.markdown("""
            **Smart Strategies:**
            - Pack versatile, mix-and-match items
            - Choose quick-dry fabrics
            - Leave room for souvenirs
            """)
        
        with tips_col3:
            st.markdown("""
            **Don't Forget:**
            - Check airline baggage limits
            - Weigh luggage before leaving
            - Keep valuables in carry-on
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Feedback Section
    st.markdown("### 🌟 Rate Your Experience")
    
    feedback_col1, feedback_col2 = st.columns([3, 1])
    
    with feedback_col1:
        rating = st.slider(
            "How satisfied are you with this travel plan?",
            1, 5, 3,
            format="%d ⭐",
            help="1 = Poor, 5 = Excellent"
        )
        
        feedback_text = st.text_area(
            "Additional comments (optional):",
            placeholder="What did you like? What could be improved?",
            height=100
        )
    
    with feedback_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("Submit Feedback", type="primary", width="stretch"):
            st.success(f"Thank you for your {rating}-star rating! 🎉")
            st.balloons()
        
        if st.button("Share Plan", width="stretch"):
            st.info("📤 Share functionality coming soon!")

# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **GlobeGenie** 🌍  
    AI Travel Planning Assistant
    
    Version 1.0.0
    """)

with footer_col2:
    st.markdown("""
    **Quick Links**
    - [Documentation](#)
    - [API Reference](#)
    - [Support](#)
    - [Privacy Policy](#)
    """)

with footer_col3:
    st.markdown("""
    **Connect With Us**
    - GitHub
    - Twitter
    - Discord
    - Email Support
    """)

st.markdown("""
<div style='text-align: center; color: #57534E; padding: 2rem 0;'>
    <p>Made with ❤️ using Streamlit | © 2024 GlobeGenie</p>
    <p style='font-size: 0.875rem;'>
        Powered by AI • Plan Smarter, Travel Better
    </p>
</div
""", unsafe_allow_html=True)