"""
GlobeGenie - AI Travel Planner
Main application entry point.
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time

# Adjust the path to include the parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from agent.input_analyzer import InputAnalyzer
from agent.orchestrator import Orchestrator
from ui.utils.styling import apply_custom_styling
from ui.utils.session_state import initialize_session_state, add_to_plan_history
from ui.components.header import render_header_section
from ui.components.sidebar import render_sidebar
from ui.components.input_section import render_input_section
from ui.components.results_section import render_results_section
from ui.components.footer import render_footer


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


# ==================== INITIALIZATION ====================
apply_custom_styling()
initialize_session_state()


# ==================== SIDEBAR ====================
with st.sidebar:
    render_sidebar()


# ==================== MAIN CONTENT ====================
# Header section
render_header_section()

# Input section
user_input, generate_clicked = render_input_section()


# ==================== PROCESSING LOGIC ====================
if generate_clicked:
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
                
                # Add to history
                add_to_plan_history(user_input, final_state)
                
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
    render_results_section(st.session_state.final_state)


# ==================== FOOTER ====================
render_footer()