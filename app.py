import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# 1. Page Configuration
st.set_page_config(page_title="Integrated Virtual Lab", layout="wide", page_icon="⚡")

# 2. Universal CSS (Applies to all pages)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #007bff; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# 3. Helpers
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# 4. Initialize Permanent Session State
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = {}
if 'completed_labs' not in st.session_state:
    st.session_state.completed_labs = {} # Dictionary: {"Exp Name": {"score": 100, "date": "..."}}

# --- LOGIN GATE ---
if not st.session_state.auth:
    col1, col2 = st.columns([1, 1])
    with col1:
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_96bovdur.json"
        st_lottie(load_lottieurl(lottie_url), height=400)
    
    with col2:
        st.title("🛡️ Student Lab Portal")
        with st.form("login"):
            name = st.text_input("Student Name")
            reg = st.text_input("Registration Number")
            dept = st.selectbox("Department", ["EEE", "ECE", "EIE", "CSE"])
            if st.form_submit_button("ENTER LABORATORY"):
                if name and reg:
                    st.session_state.user = {"name": name, "reg": reg, "dept": dept}
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Credentials required.")

# --- MAIN DASHBOARD ---
else:
    with st.sidebar:
        st.subheader(f"👨‍🎓 {st.session_state.user['name']}")
        st.caption(f"Reg: {st.session_state.user['reg']}")
        
        # Professional Navigation
        selected = option_menu(
            menu_title=None,
            options=["Home", "My Reports", "Feedback", "Logout"],
            icons=["house", "file-earmark-check", "chat-quote", "box-arrow-right"],
            styles={"container": {"padding": "0!important", "background-color": "#f8f9fa"}}
        )

    if selected == "Home":
        st.title("🏫 Virtual Lab Dashboard")
        st.markdown(f"Welcome to the **{st.session_state.user['dept']}** Virtual Lab Environment.")
        
        # Dynamic Stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Experiments Finished", len(st.session_state.completed_labs))
        c2.metric("Lab Status", "Online")
        c3.metric("Academic Year", "2025-26")
        
        st.markdown("---")
        st.subheader("📋 Instructions")
        st.info("1. Select a Subject from the sidebar list.\n2. Complete the Simulation & Quiz.\n3. Download the PDF from 'My Reports'.")

    elif selected == "My Reports":
        st.title("📄 Completed Experiment Reports")
        if not st.session_state.completed_labs:
            st.warning("No reports available. Complete an experiment first.")
        else:
            for lab, details in st.session_state.completed_labs.items():
                with st.expander(f"✅ {lab}"):
                    st.write(f"Completed on: {details.get('date', 'N/A')}")
                    st.write(f"Quiz Score: {details.get('score', 0)}%")
                    # The download button is handled within the specific pages 
                    # to ensure the data is fresh.

    elif selected == "Feedback":
        st.title("💬 Feedback")
        st.text_area("Observations or Issues:")
        if st.button("Submit"): st.success("Thank you!")

    elif selected == "Logout":
        st.session_state.auth = False
        st.rerun()
