import streamlit as st
import control as ct
import numpy as np
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# Safety Check
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Please login on the Homepage first.")
    st.stop()

st.title("🕹️ Control Systems Laboratory")

exp_type = st.sidebar.selectbox("Experiment Category", [
    "1. Time Response of Second Order System",
    "2. Stability Analysis (Bode Plot)"
])

if exp_type == "1. Time Response of Second Order System":
    st.header("Ex 1: Time Domain Analysis of Second Order System")
    
    t1, t2, t3 = st.tabs(["📖 Theory & Formulae", "📉 Simulation", "📋 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To determine the time domain specifications of a second-order system for a unit step input.")
        
        st.subheader("Standard Transfer Function")
        st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}")
        
        st.info("""
        **Key Parameters:**
        - **ωn (Natural Frequency):** The frequency at which system oscillates without damping.
        - **ζ (Damping Ratio):** Defines how the oscillations decay.
        - **Peak Overshoot (Mp):** The maximum peak value of the response curve.
        - **Settling Time (ts):** Time taken for the response to stay within 2% of the final value.
        """)

    with t2:
        st.subheader("System Configuration")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            wn = st.number_input("Natural Frequency (ωn)", value=5.0, step=0.5)
            zeta = st.slider("Damping Ratio (ζ)", 0.1, 1.5, 0.6)
            
            # Create Transfer Function: wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
            num = [wn**2]
            den = [1, 2*zeta*wn, wn**2]
            sys = ct.TransferFunction(num, den)
            
            # Calculate Step Response
            t, y = ct.step_response(sys)
            info = ct.step_info(sys)
            
            st.markdown("### Calculated Specs")
            st.metric("Rise Time (tr)", f"{info['RiseTime']:.3f} s")
            st.metric("Peak Overshoot (Mp)", f"{info['Overshoot']:.2f} %")
            st.metric("Settling Time (ts)", f"{info['SettlingTime']:.3f} s")

        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=y, name="Step Response", line=dict(color='#FF4B4B', width=3)))
            # Add a dashed line for the steady state (Unit Step = 1)
            fig.add_hline(y=1.0, line_dash="dot", line_color="green", annotation_text="Steady State")
            
            fig.update_layout(
                title=f"Step Response (ζ = {zeta})",
                xaxis_title="Time (seconds)",
                yaxis_title="Amplitude",
                hovermode="x"
            )
            st.plotly_chart(fig, use_container_width=True)

    with t3:
        st.subheader("Manual Entry & Submission")
        obs_text = st.text_area("Observations", 
                                value=f"For ωn={wn} and ζ={zeta}, the system is {'Underdamped' if zeta < 1 else 'Overdamped' if zeta > 1 else 'Critically Damped'}. "
                                f"The settling time observed is {info['SettlingTime']:.3f} seconds.")
        
        if st.button("Finalize & Generate PDF"):
            # Update Dashboard Status
            st.session_state.completed_labs["Control Systems"] = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "score": 100
            }
            
            proc = "1. Define the natural frequency and damping ratio.\n2. Generate the closed-loop transfer function.\n3. Apply a unit step input.\n4. Measure time domain specifications from the response curve."
            
            pdf_data = generate_report(
                st.session_state.user,
                "4. Control Systems Analysis",
                "To analyze the time response of a second-order system.",
                proc,
                obs_text
            )
            
            st.download_button("📩 Download Control Lab Report", data=pdf_data, file_name="Control_Systems_Report.pdf")
            st.success("Report Generated Successfully!")

elif exp_type == "2. Stability Analysis (Bode Plot)":
    st.info("Bode Plot module coming soon - utilize the Transfer Function solver for now.")
