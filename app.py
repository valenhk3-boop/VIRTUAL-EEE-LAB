import streamlit as st

st.set_page_config(page_title="Engineering Virtual Lab", layout="wide", page_icon="⚡")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.completed = []

if not st.session_state.auth:
    st.title("⚡ Engineering Virtual Laboratory")
    st.subheader("Student Access Portal")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Full Name")
            reg = st.text_input("Registration Number")
        with col2:
            dept = st.selectbox("Department", ["EEE", "ECE", "EIE", "CSE"])
            year = st.selectbox("Year", ["I", "II", "III", "IV"])
            
        if st.button("Initialize Lab Session"):
            if name and reg:
                st.session_state.user = {"name": name, "reg": reg, "dept": dept, "year": year}
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Credentials required.")
else:
    st.sidebar.title(f"👤 {st.session_state.user['name']}")
    st.sidebar.write(f"ID: {st.session_state.user['reg']}")
    
    st.title("Welcome to the Integrated Virtual Lab")
    st.markdown(f"**Department:** {st.session_state.user['dept']} | **Session:** Active")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Experiments Done", len(st.session_state.completed))
    col2.metric("Subject Modules", "4")
    col3.metric("Lab Status", "Online")

    st.success("Select a subject from the sidebar to begin your simulations.")
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
