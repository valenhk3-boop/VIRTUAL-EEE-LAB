import streamlit as st

st.set_page_config(page_title="EEE Virtual Lab", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Student Lab Portal")
    name = st.text_input("Student Name")
    reg = st.text_input("Registration Number")
    dept = st.selectbox("Department", ["Electrical & Electronics", "Electronics & Comm"])
    
    if st.button("Access Virtual Lab"):
        if name and reg:
            st.session_state.user = {"name": name, "reg": reg, "dept": dept}
            st.session_state.auth = True
            st.rerun()
else:
    st.sidebar.title(f"Welcome, {st.session_state.user['name']}")
    st.title("🏫 Virtual Engineering Laboratory")
    st.markdown("---")
    st.info("Please select a subject from the sidebar to begin your experiments.")
    
    # Progress Summary
    st.subheader("Your Progress")
    st.write("- Analog Electronics: ⏳ Pending")
    st.write("- Sensors & Instruments: ⏳ Pending")
