"""
Sidebar component with branding, stats, and help section.
"""
import streamlit as st


def render_hero_image():
    """Render the hero image at the top of sidebar"""
    st.image(
        "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&q=80", 
        use_container_width=True
    )


def render_sidebar_title():
    """Render sidebar title and branding"""
    st.title("🌍 GlobeGenie")
    st.markdown("---")


def render_welcome_section():
    """Render welcome message and how it works"""
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


def render_api_key_section():
    """
    Render API key input section.
    Currently disabled and using demo mode.
    """
    # API Key Input - DISABLED FOR NOW
    groq_api_key = "demo_mode"  # Dummy value to bypass API key checks
    
    # Uncomment below when you want to enable API key input:
    # groq_api_key = st.text_input(
    #     "Groq API Key",
    #     type="password",
    #     help="Enter your Groq API key to enable AI features"
    # )
    # return groq_api_key


def render_user_stats():
    """Render user statistics (plans created, destinations)"""
    st.markdown("#### 📊 Your Stats")
    col1, col2 = st.columns(2)
    
    # Get plan history from session state
    plan_history = st.session_state.get('plan_history', [])
    plan_count = len(plan_history)
    
    col1.metric("Plans Created", plan_count)
    col2.metric("Destinations", "0")


def render_help_section():
    """Render help and tips expander"""
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


def render_sidebar():
    """
    Render complete sidebar content.
    This is the main function to call from app.py
    """
    render_hero_image()
    render_sidebar_title()
    render_welcome_section()
    
    st.markdown("---")
    
    render_api_key_section()
    
    st.markdown("---")
    
    render_user_stats()
    
    st.markdown("---")
    
    render_help_section()