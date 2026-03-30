import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.pdf_handler import generate_report

st.title("Analog Electronics Lab")
exp = st.sidebar.selectbox("Experiment", ["Design of CE Amplifier"])

if exp == "Design of CE Amplifier":
    t1, t2, t3 = st.tabs(["Theory", "Simulation", "Assessment"])
    
    with t1:
        st.write("**Aim:** To design a Common Emitter amplifier and plot frequency response.")
        st.write("**Apparatus:** BC107, Resistors (60k, 1k, 2.2k), Capacitors (10uF).")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Common_Emitter_Amplifier.svg/500px-Common_Emitter_Amplifier.svg.png", caption="CE Amplifier Circuit")

    with t2:
        vcc = st.slider("Vcc (Voltage)", 5, 15, 12)
        freq = np.logspace(1, 6, 100)
        gain = 20 * np.log10(100 / np.sqrt(1 + (freq/500000)**2))
        
        fig = go.Figure(go.Scatter(x=freq, y=gain, mode='lines', name='Gain'))
        fig.update_xaxes(type="log", title="Frequency (Hz)")
        fig.update_yaxes(title="Gain (dB)")
        st.plotly_chart(fig)
        
        if st.button("Complete Experiment"):
            st.session_state.completed.append("CE Amplifier")
            st.success("Simulation Recorded!")

    with t3:
        if "CE Amplifier" in st.session_state.completed:
            q = st.radio("What is the phase shift in CE Amplifier?", ["0", "90", "180"])
            if st.button("Submit & Download"):
                pdf = generate_report(st.session_state.user, exp, f"Observed Gain: {max(gain):.2f} dB. Quiz Answer: {q}")
                st.download_button("Download Professional PDF", data=pdf, file_name="CE_Report.pdf")
