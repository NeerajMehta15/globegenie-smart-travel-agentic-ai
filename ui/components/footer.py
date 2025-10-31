"""
Footer component with links and information.
"""
import streamlit as st


def render_footer():
    """Render complete footer section"""
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
    </div>
    """, unsafe_allow_html=True)