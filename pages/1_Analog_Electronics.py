import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# --- Safety Check ---
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Access Denied. Please login on the Home Page.")
    st.stop()

st.title("🔬 Analog Electronics Laboratory")
st.markdown("---")

# Sidebar for Experiment Selection
exp_choice = st.sidebar.radio("Select Experiment", [
    "1. Design of CE Amplifier",
    "2. Common Base (CB) Amplifier",
    "3. RC Phase Shift Oscillator"
])

# --- EXPERIMENT 1: CE AMPLIFIER ---
if exp_choice == "1. Design of CE Amplifier":
    st.header("Experiment 1: Design of Common Emitter (CE) Amplifier")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To design a CE amplifier using self-bias configuration and plot its frequency response.")
        
        st.subheader("Apparatus Required")
        st.markdown("""
        | Item | Range | Qty |
        | :--- | :--- | :--- |
        | BC107 Transistor | NPN | 1 |
        | Resistors | 60k, 1k, 2.2k, 10k | 1 each |
        | Capacitors | 10µF | 2 |
        | Function Generator | (0-3)MHz | 1 |
        """)

        

        st.subheader("Procedure")
        proc = "1. Connect as per circuit diagram.\n2. Set Vcc=12V, Vin=20mV.\n3. Vary frequency (10Hz-1MHz).\n4. Note Vo and calculate Gain=20log(Vo/Vi)."
        st.info(proc)

    with t2:
        st.subheader("Interactive Simulation")
        vi = st.slider("Input Signal Vi (mV)", 10, 50, 20)
        f = np.logspace(1, 6, 100)
        # Model: Midband gain ~150, Fl=100Hz, Fh=500kHz
        gain_val = 150 / (np.sqrt(1 + (100/f)**2) * np.sqrt(1 + (f/500000)**2))
        gain_db = 20 * np.log10(gain_val)
        
        fig = go.Figure(go.Scatter(x=f, y=gain_db, mode='lines', line=dict(color='#007bff', width=3)))
        fig.update_xaxes(type="log", title="Frequency (Hz)")
        fig.update_yaxes(title="Gain (dB)")
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        obs = st.text_area("Observations", "Max Gain: 43dB. Bandwidth: 499.9 kHz.")
        if st.button("Finalize CE Lab"):
            st.session_state.completed_labs["CE Amplifier"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
            pdf = generate_report(st.session_state.user, "1. CE Amplifier", "Design and analysis.", proc, obs)
            st.download_button("Download PDF", data=pdf, file_name="CE_Amplifier.pdf")

# --- EXPERIMENT 2: CB AMPLIFIER ---
elif exp_choice == "2. Common Base (CB) Amplifier":
    st.header("Experiment 2: Common Base (CB) Amplifier")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To study the characteristics of a Common Base amplifier and calculate voltage gain.")
        
        st.info("**Theory:** CB amplifiers have low input impedance and high output impedance. There is 0° phase shift.")

    with t2:
        v_in_cb = st.number_input("Input Voltage (mV)", value=50)
        ie = st.slider("Emitter Current Ie (mA)", 0.5, 5.0, 1.5)
        rc = 2200 # 2.2k
        gain_cb = (ie * rc) / 26 # Simple approximation
        st.metric("Calculated Voltage Gain (Av)", f"{gain_cb:.2f}")
        
        # Static comparison graph
        f_cb = np.logspace(2, 7, 50)
        g_cb = 20 * np.log10(gain_cb / np.sqrt(1 + (f_cb/1e6)**2))
        fig2 = go.Figure(go.Scatter(x=f_cb, y=g_cb, line=dict(color='green')))
        fig2.update_xaxes(type="log", title="Frequency (Hz)")
        st.plotly_chart(fig2)

    with t3:
        if st.button("Save CB Report"):
            st.success("CB Report Ready for Dashboard.")

# --- EXPERIMENT 3: RC PHASE SHIFT OSCILLATOR ---
elif exp_choice == "3. RC Phase Shift Oscillator":
    st.header("Experiment 3: RC Phase Shift Oscillator")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To design and verify the frequency of oscillations for an RC Phase Shift Oscillator.")
        
        st.latex(r"f_o = \frac{1}{2\pi RC \sqrt{6}}")

    with t2:
        st.subheader("Design Parameters")
        c_val = st.select_slider("Capacitance (µF)", options=[0.001, 0.01, 0.1, 1.0])
        r_val = st.slider("Resistance R (Ω)", 1000, 10000, 4700)
        
        fo = 1 / (2 * np.pi * r_val * (c_val * 1e-6) * np.sqrt(6))
        st.metric("Target Frequency (fo)", f"{fo:.2f} Hz")
        
        # Sine Wave Animation
        time = np.linspace(0, 5/fo, 500)
        amplitude = np.sin(2 * np.pi * fo * time)
        fig3 = go.Figure(go.Scatter(x=time, y=amplitude, name="Output Waveform"))
        fig3.update_layout(title="Oscilloscope Output (Sine Wave)", xaxis_title="Time (s)")
        st.plotly_chart(fig3)

    with t3:
        if st.button("Download Oscillator Record"):
            pdf = generate_report(st.session_state.user, "3. RC Oscillator", "Verify Barkhausen Criterion.", "Assemble RC network.", f"Freq: {fo:.2f}Hz")
            st.download_button("Download Report", data=pdf, file_name="RC_Oscillator.pdf")
