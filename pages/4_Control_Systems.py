import streamlit as st
import control as ct
import plotly.graph_objects as go
import numpy as np

st.title("🕹️ Control Systems Stability Lab")

num_str = st.text_input("Numerator (e.g., 1)", "1")
den_str = st.text_input("Denominator (e.g., 1, 2, 1)", "1, 2, 1")

if st.button("Run Stability Analysis"):
    num = [float(x) for x in num_str.split(",")]
    den = [float(x) for x in den_str.split(",")]
    
    sys = ct.TransferFunction(num, den)
    t, y = ct.step_response(sys)
    info = ct.step_info(sys)
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Rise Time", f"{info['RiseTime']:.3f} s")
    c2.metric("Settling Time", f"{info['SettlingTime']:.3f} s")
    c3.metric("Overshoot", f"{info['Overshoot']:.1f} %")
    
    # Professional Plotly Graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, line=dict(color='#007bff', width=3)))
    fig.update_layout(title="Step Response", xaxis_title="Time (sec)", yaxis_title="Amplitude")
    st.plotly_chart(fig)
