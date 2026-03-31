import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# Safety Check & Sidebar
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Please login on the Homepage.")
    st.stop()

st.title("⚡ Analog Electronics Lab")

exp_choice = st.sidebar.radio("Lab Manual Index", [
    "Ex 1: Design of CE Amplifier", 
    "Ex 2: Common Base Amplifier"
])

if exp_choice == "Ex 1: Design of CE Amplifier":
    st.header("Experiment 1: Design of CE Amplifier")
    
    tab1, tab2, tab3 = st.tabs(["📚 Manual Details", "🧪 Virtual Workbench", "📝 Submit Report"])

    with tab1:
        st.subheader("Aim")
        st.write("To design a Common Emitter amplifier using self-bias configuration and plot the frequency response.")
        
        st.subheader("Circuit Diagram")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Common_Emitter_Amplifier.svg/500px-Common_Emitter_Amplifier.svg.png", width=500)
        
        st.subheader("Procedure")
        proc = """1. Connect the circuit as per the voltage divider bias configuration.
2. Apply Vcc = 12V and input signal Vi = 20mV.
3. Vary frequency from 10Hz to 1MHz.
4. Note down Vo and calculate Gain (dB) = 20 log10(Vo/Vi)."""
        st.info(proc)

    with tab2:
        st.subheader("Interactive Simulation")
        col1, col2 = st.columns([1, 2])
        with col1:
            vi = st.number_input("Input Voltage Vi (mV)", value=20)
            vcc = st.slider("Vcc (Supply)", 5, 15, 12)
            rl = st.number_input("Load Resistance (Ohms)", value=2200)
        
        with col2:
            f = np.logspace(1, 6, 50)
            # Theoretical CE Response
            gain_mid = 140 
            gain_db = 20 * np.log10(gain_mid / (np.sqrt(1 + (100/f)**2) * np.sqrt(1 + (f/500000)**2)))
            
            fig = go.Figure(go.Scatter(x=f, y=gain_db, mode='lines+markers', name='Frequency Response'))
            fig.update_xaxes(type="log", title="Frequency (Hz)")
            fig.update_yaxes(title="Gain (dB)")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Result Generation")
        obs = st.text_area("Enter Observations", "Max Gain observed at 1kHz. Bandwidth found to be approx 450kHz.")
        
        if st.button("Generate & Save Record"):
            # Update the main dashboard's completed list
            st.session_state.completed_labs["CE Amplifier"] = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "score": 100
            }
            
            report_pdf = generate_report(
                st.session_state.user, 
                "1. CE Amplifier",
                "To design and analyze frequency response of CE Amplifier.",
                proc,
                obs
            )
            st.download_button("📩 Download Final Lab Record", data=report_pdf, file_name="CE_Amplifier_Record.pdf")
            st.success("Record saved to 'My Reports' in Dashboard.")
