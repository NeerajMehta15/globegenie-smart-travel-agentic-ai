"""
Header section components.
Includes page title, gradient header, and feature cards.
"""
import streamlit as st


def render_page_title():
    """Render main page title"""
    st.title("🌍 GlobeGenie - AI Travel Planner")


def render_gradient_header():
    """Render the gradient header box with tagline"""
    st.markdown("""
    <div class='gradient-header'>
        <h3>Plan Your Perfect Journey with AI</h3>
        <p>From budget backpacking to luxury escapes - personalized itineraries in seconds</p>
    </div>
    """, unsafe_allow_html=True)


def render_feature_cards():
    """Render the 4 feature highlight cards"""
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


def render_header_section():
    """
    Render complete header section.
    This is the main function to call from app.py
    """
    render_page_title()
    render_gradient_header()
    render_feature_cards()
    st.markdown("<br>", unsafe_allow_html=True)