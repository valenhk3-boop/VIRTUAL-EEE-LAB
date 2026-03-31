import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# Safety Check
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Please login on the Homepage.")
    st.stop()

st.title("🛠️ Sensors & Instrumentation Lab")

# Sidebar Experiment Selection
exp_choice = st.sidebar.selectbox("Experiment List", [
    "Ex 1: Loading Effect of Potentiometer",
    "Ex 2: Strain Gauge Analysis"
])

if exp_choice == "Ex 1: Loading Effect of Potentiometer":
    st.header("Ex 1: Loading Effect of Potentiometer")
    
    t1, t2, t3 = st.tabs(["📖 Lab Manual", "🕹️ Virtual Simulation", "📝 Generate Record"])

    with t1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Aim")
            st.write("To verify the loading effect of the given Potentiometer.")
            st.subheader("Apparatus")
            st.markdown("- Potentiometer (4000Ω)\n- RPS (0-30V)\n- Voltmeter (0-30V)\n- Load Resistors")
        with col2:
            # You can replace this URL with a screenshot from your SL Lab PDF
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Potentiometer_as_voltage_divider.svg/300px-Potentiometer_as_voltage_divider.svg.png", caption="Potentiometer Circuit")

        st.subheader("Procedure")
        proc_text = """1. Connect the RPS (10V) to the fixed terminals of the Potentiometer.
2. Connect a voltmeter to the variable terminal (wiper).
3. Measure Vout for different wiper positions (k) from 0.1 to 1.0.
4. Repeat the process by connecting a Load Resistor (Rl) in parallel to the output.
5. Observe the drop in voltage due to the loading effect."""
        st.info(proc_text)

    with t2:
        st.subheader("Virtual Test Bench")
        c1, c2 = st.columns(2)
        with c1:
            vin = st.slider("Input Voltage (Vin)", 5, 20, 10)
            rp = 4000 # Pot resistance from your manual
            rl = st.select_slider("Load Resistance (Rl) in Ohms", options=[1000, 5000, 10000, 100000], value=5000)
        
        # Calculations
        k = np.linspace(0.1, 1.0, 10)
        v_ideal = vin * k
        # Loading Effect Formula
        v_actual = vin * (k / (1 + (k * (1 - k) * (rp / rl))))
        
        df = pd.DataFrame({
            "Wiper Position (k)": k,
            "Ideal Vout (V)": np.round(v_ideal, 2),
            "Actual Vout (V)": np.round(v_actual, 2),
            "Error (V)": np.round(v_ideal - v_actual, 2)
        })

        with c2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=k, y=v_ideal, name="Ideal (No Load)", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=k, y=v_actual, name=f"Actual (Load={rl}Ω)"))
            fig.update_layout(title="Loading Effect Graph", xaxis_title="k", yaxis_title="Output Voltage (V)")
            st.plotly_chart(fig, use_container_width=True)
        
        st.table(df)

    with t3:
        st.subheader("Laboratory Submission")
        conclusion = st.text_area("Conclusion", value="The output voltage decreases as the load resistance decreases, verifying the loading effect.")
        
        if st.button("Verify & Print Report"):
            st.session_state.completed_labs["Potentiometer Lab"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
            
            pdf_file = generate_report(
                st.session_state.user, 
                "1. Potentiometer Loading",
                "To verify the loading effect of a potentiometer.",
                proc_text,
                f"Load Resistance: {rl} Ohms. {conclusion}"
            )
            st.download_button("Download Signed PDF", data=pdf_file, file_name="Potentiometer_Lab.pdf")
