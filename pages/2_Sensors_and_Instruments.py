import streamlit as st
import control as ct
import plotly.graph_objects as go
from utils.pdf_handler import generate_report

st.title("Control Systems Stability")

num = st.text_input("Numerator (e.g. 1)", "1")
den = st.text_input("Denominator (e.g. 1, 10, 20)", "1, 10, 20")

if st.button("Analyze Stability"):
    n = [float(x) for x in num.split(",")]
    d = [float(x) for x in den.split(",")]
    sys = ct.TransferFunction(n, d)
    t, y = ct.step_response(sys)
    info = ct.step_info(sys)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Overshoot", f"{info['Overshoot']:.2f}%")
    col2.metric("Settling Time", f"{info['SettlingTime']:.2f}s")
    col3.metric("Rise Time", f"{info['RiseTime']:.2f}s")
    
    fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='red')))
    st.plotly_chart(fig)
