import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# Page Configuration
st.set_page_config(page_title="Integrated Virtual Engineering Lab", layout="wide", page_icon="⚡")

# Function to load Lottie Animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Engineering Animation URL
lottie_eng = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_96bovdur.json") 

# Enhanced Professional CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stMetricValue"] { font-size: 2rem; color: #007bff; font-weight: 700; }
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 8px;
        height: 3em;
        background: linear-gradient(45deg, #007bff, #0056b3);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# Session State Initialization
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'completed' not in st.session_state:
    st.session_state.completed = []

# --- LOGIN SCREEN ---
if not st.session_state.auth:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st_lottie(lottie_eng, height=400, key="coding")
        
    with col2:
        st.title("⚡ Virtual Lab Portal")
        st.markdown("### Student Access Login")
        
        with st.form("login_form"):
            name = st.text_input("Full Name")
            reg = st.text_input("Registration Number (Reg. No)")
            dept = st.selectbox("Department", ["Electrical & Electronics (EEE)", "Electronics & Comm (ECE)", "Instrumentation (EIE)"])
            
            submit = st.form_submit_button("INITIALIZE SESSION")
            
            if submit:
                if name and reg:
                    st.session_state.user = {"name": name, "reg": reg, "dept": dept}
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Please provide all credentials to enter the lab.")

# --- DASHBOARD SCREEN ---
else:
    # Professional Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 {st.session_state.user['name']}")
        st.caption(f"ID: {st.session_state.user['reg']}")
        st.markdown("---")
        
        # This replaces the standard sidebar list with a professional menu
        selected = option_menu(
            menu_title="Main Menu",
            options=["Dashboard", "Lab Manual", "Feedback", "Logout"],
            icons=["house", "book", "chat-left-dots", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Dashboard":
        st.title("🏛️ Integrated Virtual Lab Dashboard")
        st.markdown(f"Welcome back, **{st.session_state.user['name']}**. All system modules are active.")
        
        # Metric Cards
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Experiments Completed", len(st.session_state.completed))
        with m_col2:
            st.metric("Total Modules", "5")
        with m_col3:
            st.metric("System Health", "100%")

        st.markdown("---")
        
        # Action Center
        st.subheader("🚀 Quick Start")
        st.info("Use the sidebar on the left to navigate between different Subjects and Experiments.")
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            <div class='main-card'>
                <h4>Instructions</h4>
                <ul>
                    <li>Select a subject from the file list on the sidebar.</li>
                    <li>Complete the interactive simulation to unlock the quiz.</li>
                    <li>Score 100% on the quiz to download your professional PDF report.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[1]:
             if len(st.session_state.completed) > 0:
                 st.success(f"Last Activity: {st.session_state.completed[-1]} finished.")
             else:
                 st.warning("No activity recorded in this session yet.")

    elif selected == "Feedback":
        st.header("📋 Lab Feedback Form")
        st.write("Help us improve the virtual lab experience.")
        with st.form("feedback"):
            rating = st.slider("Rate the UI Experience", 1, 5, 5)
            comments = st.text_area("Suggestions for improvements")
            if st.form_submit_button("Submit Review"):
                st.balloons()
                st.success("Thank you for your feedback!")

    elif selected == "Logout":
        st.session_state.auth = False
        st.rerun()
