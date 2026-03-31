import streamlit as st
import control as ct
import numpy as np
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# --- Safety Check ---
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Access Denied. Please login on the Home Page.")
    st.stop()

st.title("🕹️ Control Systems Laboratory")
st.markdown("---")

exp_choice = st.sidebar.radio("Select Experiment", [
    "1. Time Response of Second Order System",
    "2. Stability Analysis using Bode Plot",
    "3. Root Locus Construction"
])

# --- EXPERIMENT 1: TIME RESPONSE ---
if exp_choice == "1. Time Response of Second Order System":
    st.header("Ex 1: Time Domain Analysis of Second Order System")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "📈 Simulation", "📝 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To determine the time domain specifications (Rise time, Peak time, Settling time) of a second-order system.")
        
        st.subheader("Standard Equation")
        st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}")
        
        
        
        st.subheader("Procedure")
        proc = "1. Define ωn and ζ.\n2. Obtain the closed-loop transfer function.\n3. Apply unit step input.\n4. Calculate specifications from the response."
        st.info(proc)

    with t2:
        col1, col2 = st.columns([1, 2])
        with col1:
            wn = st.number_input("Natural Frequency (ωn)", 1.0, 20.0, 5.0)
            zeta = st.slider("Damping Ratio (ζ)", 0.1, 1.5, 0.6)
            
            num = [wn**2]
            den = [1, 2*zeta*wn, wn**2]
            sys = ct.TransferFunction(num, den)
            t, y = ct.step_response(sys)
            info = ct.step_info(sys)
            
            st.metric("Rise Time (tr)", f"{info['RiseTime']:.3f} s")
            st.metric("Peak Overshoot (Mp)", f"{info['Overshoot']:.2f} %")
            st.metric("Settling Time (ts)", f"{info['SettlingTime']:.3f} s")

        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=y, line=dict(color='#FF4B4B', width=3)))
            fig.add_hline(y=1.0, line_dash="dot", line_color="green")
            fig.update_layout(title="Step Response", xaxis_title="Time (s)", yaxis_title="Amplitude")
            st.plotly_chart(fig, use_container_width=True)

    with t3:
        if st.button("Generate Time Response Report"):
            st.session_state.completed_labs["Time Response"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
            pdf = generate_report(st.session_state.user, "4.1 Time Response", "Analyze 2nd order system.", proc, f"Verified for wn={wn}, zeta={zeta}.")
            st.download_button("Download PDF", data=pdf, file_name="Time_Response.pdf")

# --- EXPERIMENT 2: BODE PLOT ---
elif exp_choice == "2. Stability Analysis using Bode Plot":
    st.header("Ex 2: Frequency Response & Stability (Bode Plot)")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "📉 Frequency Analysis", "📝 Lab Record"])

    with t1:
        st.write("**Aim:** To find the Gain Margin (GM) and Phase Margin (PM) using Bode Plot.")
        
        st.info("**Stability Criterion:** For a stable system, both GM and PM must be positive.")

    with t2:
        k = st.number_input("System Gain (K)", 1, 1000, 100)
        # G(s) = K / [s(s+1)(s+10)]
        num = [k]
        den = [1, 11, 10, 0]
        sys = ct.TransferFunction(num, den)
        
        mag, phase, omega = ct.bode(sys, plot=False)
        gm, pm, wg, wp = ct.margin(sys)
        
        st.subheader("Stability Metrics")
        c1, c2 = st.columns(2)
        c1.metric("Gain Margin (GM)", f"{20*np.log10(gm):.2f} dB")
        c2.metric("Phase Margin (PM)", f"{pm:.2f} °")
        
        fig_mag = go.Figure(go.Scatter(x=omega, y=20*np.log10(mag), name="Magnitude"))
        fig_mag.update_xaxes(type="log", title="Frequency (rad/s)")
        fig_mag.update_yaxes(title="Magnitude (dB)")
        st.plotly_chart(fig_mag, use_container_width=True)

    with t3:
        if st.button("Save Bode Stability Data"):
            st.success("Stability analysis recorded.")

# --- EXPERIMENT 3: ROOT LOCUS ---
elif exp_choice == "3. Root Locus Construction":
    st.header("Ex 3: Effect of Gain on Stability (Root Locus)")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🎡 Root Locus Explorer", "📝 Lab Record"])

    with t1:
        st.write("**Aim:** To plot the root locus for a given open-loop transfer function.")
        
        st.info("**Significance:** Root locus shows how the closed-loop poles move as gain K varies from 0 to ∞.")

    with t2:
        # Example: G(s) = K / [s(s+2)(s+4)]
        sys_rl = ct.TransferFunction([1], [1, 6, 8, 0])
        rlist, klist = ct.root_locus(sys_rl, plot=False)
        
        fig_rl = go.Figure()
        for i in range(rlist.shape[1]):
            fig_rl.add_trace(go.Scatter(x=np.real(rlist[:,i]), y=np.imag(rlist[:,i]), name=f"Branch {i+1}"))
        
        fig_rl.update_layout(title="Root Locus Plot", xaxis_title="Real", yaxis_title="Imaginary")
        st.plotly_chart(fig_rl, use_container_width=True)

    with t3:
        if st.button("Finalize Root Locus Lab"):
            st.balloons()
