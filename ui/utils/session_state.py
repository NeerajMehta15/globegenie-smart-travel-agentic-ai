"""
Session state management for the application.
"""
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
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


def reset_results():
    """Clear results and generated prompt"""
    st.session_state.show_results = False
    st.session_state.generated_prompt = ""


def add_to_plan_history(user_input, final_state):
    """Add a completed plan to history"""
    from datetime import datetime
    
    st.session_state.plan_history.append({
        'date': datetime.now(),
        'input': user_input[:100] + '...' if len(user_input) > 100 else user_input,
        'state': final_state
    })