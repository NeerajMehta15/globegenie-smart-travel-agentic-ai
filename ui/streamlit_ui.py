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

# ==================== CUSTOM CSS STYLING - DARK THEME ====================
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - Dark Background */
    .main {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #F1F5F9;
        font-weight: 700;
        padding-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #E2E8F0;
        font-weight: 600;
        padding-top: 1rem;
    }
    
    h3 {
        color: #CBD5E1;
        font-weight: 500;
    }
    
    /* Gradient Header Box */
    .gradient-header {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
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
        background: #1E293B;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: #283548;
        border-color: #475569;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .feature-card h3 {
        color: #F1F5F9;
        margin-top: 0;
        font-size: 1.1rem;
    }
    
    .feature-card p {
        color: #94A3B8;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #5568D3 0%, #6941A8 100%);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
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
        background-color: #1E293B;
        border: 2px solid #334155;
        border-radius: 8px;
        color: #E2E8F0;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #667EEA;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background-color: #283548;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #64748B;
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
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        background-color: #667EEA;
    }
    
    .stSlider>div>div>div {
        background-color: #334155;
    }
    
    /* Radio Buttons */
    .stRadio>div {
        background-color: transparent;
    }
    
    .stRadio>div>label>div {
        background-color: #1E293B;
        border: 2px solid #334155;
        color: #E2E8F0;
    }
    
    .stRadio>div>label>div:hover {
        border-color: #667EEA;
        background-color: #283548;
    }
    
    /* Multiselect */
    .stMultiselect>div>div>div {
        background-color: #1E293B;
        border: 2px solid #334155;
    }
    
    .stMultiselect span {
        color: #E2E8F0;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667EEA;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94A3B8;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10B981;
    }
    
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #94A3B8;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #283548;
        color: #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #E2E8F0;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #283548;
        border-color: #475569;
    }
    
    .streamlit-expanderContent {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Alert Boxes */
    .stAlert {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #E2E8F0;
    }
    
    div[data-baseweb="notification"] {
        background-color: #1E293B;
        border-left-width: 4px;
    }
    
    /* Success */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left-color: #10B981;
    }
    
    /* Info */
    .stInfo {
        background-color: rgba(102, 126, 234, 0.1);
        border-left-color: #667EEA;
    }
    
    /* Warning */
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
    }
    
    /* Error */
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left-color: #EF4444;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }
    
    /* Progress Bar */
    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #667EEA 0%, #764BA2 100%);
    }
    
    .stProgress>div>div>div {
        background-color: #334155;
    }
    
    /* Spinner */
    .stSpinner>div {
        border-top-color: #667EEA;
    }
    
    /* Custom Info Box */
    .info-box {
        background-color: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667EEA;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #E2E8F0;
    }
    
    .info-box strong {
        color: #A5B4FC;
    }
    
    /* Divider */
    hr {
        border-color: #334155;
    }
    
    /* Download Button */
    .stDownloadButton>button {
        background-color: #1E293B;
        border: 2px solid #334155;
        color: #E2E8F0;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background-color: #283548;
        border-color: #667EEA;
    }
    
    /* Form */
    .stForm {
        background-color: transparent;
        border: none;
    }
    
    /* Checkbox */
    .stCheckbox>label>span {
        color: #CBD5E1;
    }
    
    /* Date Input */
    .stDateInput>div>div>input {
        background-color: #1E293B;
        border: 2px solid #334155;
        color: #E2E8F0;
    }
    
    /* Remove Streamlit branding color */
    .css-1d391kg, .css-fg4pbf {
        background-color: #0F172A;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1E293B;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748B;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        background-color: #1E293B;
        border-radius: 8px;
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
    
    # API Key Input
    st.markdown("#### 🔑 Configuration")
    groq_api_key = st.text_input(
        "Groq API Key:",
        type="password",
        help="Enter your Groq API key to enable AI planning features",
        placeholder="gsk_..."
    )
    
    if groq_api_key:
        st.success("✅ API Key configured")
    else:
        st.info("ℹ️ API key required for trip generation")
    
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
            st.session_state.generated_prompt = user_input
            st.session_state.input_method = "detailed"

# ==================== GENERATE BUTTON (for quick input) ====================
if st.session_state.input_method == "quick" and user_input_quick:
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        generate_button = st.button(
            "🚀 Generate Travel Plan",
            type="primary",
            use_container_width=True,
            disabled=not groq_api_key,
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
    if not groq_api_key:
        st.error("❌ Please enter your Groq API key in the sidebar to continue")
    elif not user_input or len(user_input.strip()) < 20:
        st.warning("⚠️ Please provide more details about your trip (at least 20 characters)")
    else:
        # Validation passed - show processing
        st.markdown("---")
        
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            st.markdown("""
            <div style='background-color: rgba(102, 126, 234, 0.1); padding: 1.5rem; 
                        border-radius: 12px; border-left: 4px solid #667EEA;'>
                <h4 style='margin-top: 0; color: #A5B4FC;'>
                    ✨ Creating Your Perfect Itinerary
                </h4>
                <p style='margin-bottom: 0; color: #CBD5E1;'>
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
                time.sleep(0.5)  # Simulated delay
            
            # Actual workflow execution would go here
            # The user_input variable now contains the prompt (either from quick or detailed form)
            # try:
            #     analyzer = InputAnalyzer()
            #     trip_state = analyzer.process_input(user_input)  # Pass the prompt
            #     
            #     orchestrator = Orchestrator()
            #     final_state = orchestrator.orchestrate_trip_planning(trip_state)
            #     
            #     st.session_state.final_state = final_state
            #     st.session_state.show_results = True
            #     st.session_state.plan_history.append({
            #         'date': datetime.now(),
            #         'input': user_input[:100] + '...',
            #         'state': final_state
            #     })
            #     
            # except Exception as e:
            #     st.error(f"❌ Error generating plan: {str(e)}")
            #     st.session_state.show_results = False
            
            # For demo purposes
            status_text.empty()
            progress_bar.empty()
            
            st.balloons()  # Celebration!
            
            st.success("✅ Your personalized travel plan is ready!")
            
            # Show demo message
            st.info(f"""
            🔧 **Demo Mode Active**
            
            **Your Prompt:** {user_input[:200]}{'...' if len(user_input) > 200 else ''}
            
            Workflow execution is currently disabled to save tokens. 
            In production, this prompt would be sent to your AI agent for processing.
            
            Enable the workflow in the code to see full results!
            """)

# ==================== RESULTS DISPLAY ====================
if st.session_state.get('show_results', False) and st.session_state.final_state:
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Success header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
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
            use_container_width=True
        )
    
    with col2:
        st.button("📧 Email Plan", use_container_width=True)
    
    with col3:
        st.button("🔄 Modify Plan", use_container_width=True)
    
    with col4:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.generated_prompt = ""
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("### 📊 Trip Summary at a Glance")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    budget_summary = final_state.final_plan.get('budget_summary', {})
    
    with metric_col1:
        st.metric(
            label="Total Cost",
            value=f"${budget_summary.get('total_cost', 4250)}",
            delta=f"-${budget_summary.get('savings', 150)}",
            delta_color="inverse"
        )
    
    with metric_col2:
        st.metric(
            label="Duration",
            value="7 days",
            delta="Perfect length"
        )
    
    with metric_col3:
        st.metric(
            label="Per Person",
            value=f"${budget_summary.get('per_person', 2125)}",
            delta="Within budget"
        )
    
    with metric_col4:
        st.metric(
            label="Activities",
            value=len(final_state.final_plan.get('itinerary', [])) * 4,
            delta="+5 optional"
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
        
        trip_summary = final_state.final_plan.get('trip_summary', 
            "Experience the perfect blend of adventure and relaxation on this carefully curated journey.")
        
        st.markdown(f"""
        <div style='background-color: #1E293B; padding: 1.5rem; 
                    border-radius: 8px; border-left: 4px solid #667EEA;'>
            <p style='font-size: 1.1rem; line-height: 1.7; margin: 0; color: #E2E8F0;'>
                {trip_summary}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Destination Research
        if final_state.destination_research:
            st.markdown("### 🏆 Top Attractions & Highlights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Must-See Attractions")
                attractions = final_state.destination_research.get('attractions', [
                    "Historical Old Town",
                    "National Museum",
                    "Scenic Viewpoint",
                    "Local Market",
                    "Waterfront Promenade"
                ])
                
                for i, attraction in enumerate(attractions[:5], 1):
                    st.markdown(f"**{i}.** {attraction}")
            
            with col2:
                st.markdown("#### Local Experiences")
                experiences = final_state.destination_research.get('experiences', [
                    "Traditional cooking class",
                    "Guided walking tour",
                    "Sunset boat cruise",
                    "Wine tasting experience",
                    "Local craft workshop"
                ])
                
                for i, exp in enumerate(experiences[:5], 1):
                    st.markdown(f"**{i}.** {exp}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Best Time to Visit
        st.markdown("### 🌤️ Weather & Best Time")
        
        weather_col1, weather_col2 = st.columns(2)
        
        with weather_col1:
            st.markdown("""
            **Expected Weather:**
            - Temperature: 22-28°C (72-82°F)
            - Conditions: Sunny with occasional clouds
            - Rainfall: Low (5 days/month average)
            """)
        
        with weather_col2:
            st.markdown("""
            **What to Expect:**
            - Peak tourist season
            - Higher accommodation prices
            - Festivals and local events
            - Advance booking recommended
            """)
    
    # TAB 2: Itinerary
    with tab2:
        st.markdown("### 📅 Your Day-by-Day Adventure")
        
        itinerary = final_state.final_plan.get('itinerary', [
            {
                'day': 1,
                'theme': 'Arrival & City Exploration',
                'activities': [
                    {'time': '10:00 AM', 'activity': 'Airport pickup & hotel check-in', 
                     'location': 'City Center Hotel', 'duration': '2 hours', 
                     'estimated_cost': 50, 'notes': 'Private transfer included'},
                    {'time': '2:00 PM', 'activity': 'Walking tour of Old Town', 
                     'location': 'Historic District', 'duration': '3 hours', 
                     'estimated_cost': 25, 'notes': 'English-speaking guide'},
                    {'time': '7:00 PM', 'activity': 'Welcome dinner at local restaurant', 
                     'location': 'Waterfront Area', 'duration': '2 hours', 
                     'estimated_cost': 80, 'notes': 'Traditional cuisine'}
                ],
                'total_day_cost': 155
            },
            {
                'day': 2,
                'theme': 'Cultural Immersion',
                'activities': [
                    {'time': '9:00 AM', 'activity': 'Visit National Museum', 
                     'location': 'Museum District', 'duration': '3 hours', 
                     'estimated_cost': 20, 'notes': 'Skip-the-line tickets'},
                    {'time': '1:00 PM', 'activity': 'Lunch at traditional cafe', 
                     'location': 'Arts Quarter', 'duration': '1.5 hours', 
                     'estimated_cost': 35, 'notes': 'Vegetarian options available'},
                    {'time': '3:00 PM', 'activity': 'Cooking class experience', 
                     'location': 'Culinary School', 'duration': '3 hours', 
                     'estimated_cost': 75, 'notes': 'Hands-on class with dinner'},
                ],
                'total_day_cost': 130
            }
        ])
        
        for day_plan in itinerary:
            with st.expander(
                f"**Day {day_plan['day']}:** {day_plan.get('theme', 'Activities')} "
                f"(${day_plan.get('total_day_cost', 0)})",
                expanded=(day_plan['day'] == 1)
            ):
                for activity in day_plan.get('activities', []):
                    st.markdown(f"""
                    <div style='background-color: #1E293B; padding: 1rem; 
                                margin-bottom: 1rem; border-radius: 8px; 
                                border-left: 3px solid #667EEA;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #A5B4FC;'>
                            ⏰ {activity['time']} - {activity['activity']}
                        </h4>
                        <p style='margin: 0.25rem 0; color: #94A3B8;'>
                            <strong>📍 Location:</strong> {activity['location']}<br>
                            <strong>⏱️ Duration:</strong> {activity['duration']}<br>
                            <strong>💵 Cost:</strong> ${activity['estimated_cost']}
                        </p>
                        {f"<p style='margin: 0.5rem 0 0 0; font-style: italic; color: #64748B;'>💡 {activity.get('notes', '')}</p>" if activity.get('notes') else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='text-align: right; font-weight: 600; color: #10B981; 
                            padding-top: 0.5rem; border-top: 2px solid #334155;'>
                    Total Day Cost: ${day_plan.get('total_day_cost', 0)}
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 3: Budget
    with tab3:
        st.markdown("### 💰 Complete Budget Analysis")
        
        budget_summary = final_state.final_plan.get('budget_summary', {
            'total_cost': 4250,
            'per_person': 2125,
            'breakdown': {
                'accommodation': 1400,
                'food': 980,
                'activities': 650,
                'transportation': 720,
                'miscellaneous': 500
            }
        })
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Budget", f"${budget_summary.get('total_cost', 0)}")
        
        with col2:
            st.metric("Per Person", f"${budget_summary.get('per_person', 0)}")
        
        with col3:
            daily_avg = budget_summary.get('total_cost', 0) // 7
            st.metric("Daily Average", f"${daily_avg}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Budget breakdown
        if 'breakdown' in budget_summary:
            st.markdown("#### 📊 Cost by Category")
            
            breakdown = budget_summary['breakdown']
            
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
                    percentage = (amount / total) * 100
                    st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <strong style='color: #CBD5E1;'>{category.replace('_', ' ').title()}</strong><br>
                        <span style='font-size: 1.2rem; color: #667EEA;'>${amount}</span>
                        <span style='color: #94A3B8;'> ({percentage:.1f}%)</span>
                    </div>
                    """, unsafe_allow_html=True)
        
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
        
        essentials = final_state.final_plan.get('travel_essentials', {
            'visa': 'Tourist visa required (apply 4 weeks in advance)',
            'insurance': 'Travel insurance strongly recommended',
            'currency': 'Local currency: EUR (1 USD = 0.92 EUR)',
            'weather': 'Mild and pleasant, pack layers',
            'language': 'English widely spoken in tourist areas',
            'timezone': 'GMT+2 (7 hours ahead of EST)'
        })
        
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
        
        packing_list = final_state.final_plan.get('packing_list', {
            'Clothing': [
                'Comfortable walking shoes',
                'Casual day outfits (5-7)',
                'Light jacket or sweater',
                'Swimwear',
                'One dressy outfit',
                'Undergarments and socks'
            ],
            'Electronics': [
                'Phone and charger',
                'Power adapter/converter',
                'Portable power bank',
                'Camera (optional)',
                'Headphones',
                'E-reader/tablet'
            ],
            'Toiletries': [
                'Toothbrush and toothpaste',
                'Shampoo and soap',
                'Sunscreen (SPF 30+)',
                'Personal medications',
                'Basic first-aid supplies',
                'Hand sanitizer'
            ],
            'Documents': [
                'Passport and copies',
                'Travel insurance documents',
                'Flight confirmations',
                'Hotel reservations',
                'Emergency contacts',
                'Credit cards and cash'
            ],
            'Other Essentials': [
                'Reusable water bottle',
                'Day backpack',
                'Travel pillow',
                'Zip-lock bags',
                'Pen for forms',
                'Snacks for travel'
            ]
        })
        
        # Organize packing list by category
        pack_col1, pack_col2 = st.columns(2)
        
        categories = list(packing_list.keys())
        mid_point = len(categories) // 2
        
        with pack_col1:
            for category in categories[:mid_point + 1]:
                st.markdown(f"#### {category}")
                items = packing_list[category]
                for item in items:
                    checked = st.checkbox(item, key=f"pack_{category}_{item}")
                st.markdown("<br>", unsafe_allow_html=True)
        
        with pack_col2:
            for category in categories[mid_point + 1:]:
                st.markdown(f"#### {category}")
                items = packing_list[category]
                for item in items:
                    checked = st.checkbox(item, key=f"pack_{category}_{item}")
                st.markdown("<br>", unsafe_allow_html=True)
        
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
        
        if st.button("Submit Feedback", type="primary", use_container_width=True):
            st.success(f"Thank you for your {rating}-star rating! 🎉")
            st.balloons()
            # TODO: Save feedback to database
        
        if st.button("Share Plan", use_container_width=True):
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
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p>Made with ❤️ using Streamlit | © 2024 GlobeGenie</p>
    <p style='font-size: 0.875rem;'>
        Powered by AI • Plan Smarter, Travel Better
    </p>
</div>
""", unsafe_allow_html=True)