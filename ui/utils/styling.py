"""
Custom CSS styling for the application.
Contains all Anthropic-themed styles.
"""
import streamlit as st


def get_custom_css():
    """Returns complete custom CSS as a string"""
    return """
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

    .st-chip-accent {
        background-color: #D97757 !important;
        color: white !important;
        border-color: #D97757 !important;
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
        background-color: rgba(217, 119, 87, 0.1);
        border-left-color: #D97757;
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
        color: #FFD6B0 !important;
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
    """


def apply_custom_styling():
    """Applies custom CSS to the Streamlit app"""
    st.markdown(get_custom_css(), unsafe_allow_html=True)