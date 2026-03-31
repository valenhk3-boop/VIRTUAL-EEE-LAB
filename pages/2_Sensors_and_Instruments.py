import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.pdf_handler import generate_report
from datetime import datetime

# --- Safety Check ---
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Access Denied. Please login on the Home Page.")
    st.stop()

st.title("🛠️ Sensors & Instrumentation Lab")
st.markdown("---")

exp_choice = st.sidebar.radio("Select Experiment", [
    "1. Loading Effect of Potentiometer",
    "2. Strain Gauge Characteristics",
    "3. LVDT Displacement Sensor"
])

# --- EXPERIMENT 1: POTENTIOMETER ---
if exp_choice == "1. Loading Effect of Potentiometer":
    st.header("Ex 1: Loading Effect of Potentiometer")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.subheader("Aim")
        st.write("To verify the loading effect of the given Potentiometer by comparing ideal and actual output voltages.")
        
        st.subheader("Apparatus Required")
        st.markdown("- Potentiometer (4kΩ)\n- RPS (0-30V)\n- Voltmeter (0-30V)\n- Load Resistor Bank")
        
        
        
        st.subheader("Theory")
        st.info("A potentiometer acts as a voltage divider. Ideally, $V_{out} = k \cdot V_{in}$. However, when a load $R_L$ is connected, it draws current, causing the output voltage to drop. This error is maximum at $k \approx 0.67$.")

    with t2:
        st.subheader("Interactive Simulation")
        col1, col2 = st.columns([1, 2])
        with col1:
            vin = st.number_input("Input Voltage (V)", 5, 30, 10)
            rp = 4000 # 4k Pot
            rl = st.select_slider("Load Resistance (Ω)", options=[1000, 5000, 10000, 100000], value=5000)
        
        k = np.linspace(0, 1, 11)
        v_ideal = vin * k
        # Loading Formula: Vo = Vin * [k / (1 + k(1-k)(Rp/Rl))]
        v_actual = vin * (k / (1 + k * (1 - k) * (rp / rl)))
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=k, y=v_ideal, name="Ideal (No Load)", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=k, y=v_actual, name=f"Actual (Load={rl}Ω)", line=dict(width=3)))
            fig.update_layout(title="Vout vs Wiper Position (k)", xaxis_title="k", yaxis_title="Voltage (V)")
            st.plotly_chart(fig, use_container_width=True)

    with t3:
        df = pd.DataFrame({"k": k, "Ideal V": v_ideal, "Actual V": np.round(v_actual, 2)})
        st.table(df)
        if st.button("Generate Potentiometer Report"):
            st.session_state.completed_labs["Potentiometer"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
            pdf = generate_report(st.session_state.user, "2.1 Potentiometer", "Verify loading effect.", "Connect load and vary k.", f"Observed error at RL={rl} ohms.")
            st.download_button("Download PDF", data=pdf, file_name="Potentiometer_Lab.pdf")

# --- EXPERIMENT 2: STRAIN GAUGE ---
elif exp_choice == "2. Strain Gauge Characteristics":
    st.header("Ex 2: Analysis of Strain Gauge Characteristics")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.write("**Aim:** To study the relationship between applied load and output voltage in a strain gauge bridge.")
        
        st.info("**Theory:** Strain gauges use the piezoresistive effect. When force is applied, resistance changes: $\Delta R = G \cdot \epsilon \cdot R$, where G is the Gauge Factor.")

    with t2:
        gf = st.slider("Gauge Factor (G)", 1.5, 2.5, 2.0)
        weight = st.slider("Applied Load (kg)", 0, 10, 0)
        # Simulated Bridge Output
        v_bridge = (weight * gf * 0.5) # Arbitrary linear model for simulation
        
        st.metric("Bridge Output Voltage", f"{v_bridge:.3f} mV")
        
        # Calibration Curve
        w_range = np.linspace(0, 10, 20)
        v_range = w_range * gf * 0.5
        fig2 = go.Figure(go.Scatter(x=w_range, y=v_range, mode='lines+markers', line=dict(color='red')))
        fig2.update_layout(title="Calibration Curve", xaxis_title="Load (kg)", yaxis_title="Output (mV)")
        st.plotly_chart(fig2)

    with t3:
        if st.button("Save Strain Gauge Data"):
            st.success("Calibration data saved to session.")

# --- EXPERIMENT 3: LVDT ---
elif exp_choice == "3. LVDT Displacement Sensor":
    st.header("Ex 3: Characteristics of LVDT")
    t1, t2, t3 = st.tabs(["📖 Manual Details", "🕹️ Virtual Workbench", "📝 Lab Record"])

    with t1:
        st.write("**Aim:** To measure displacement using Linear Variable Differential Transformer (LVDT).")
        
        st.write("**Procedure:** 1. Set the core to Null Position (0V). 2. Move core in steps of 1mm. 3. Note differential output $V_{s1} - V_{s2}$.")

    with t2:
        disp = st.slider("Core Displacement (mm)", -20, 20, 0)
        # LVDT Model: Linear within range, phase shift at null
        v_out_lvdt = disp * 0.25 # 0.25V per mm
        
        st.subheader("LVDT Output")
        st.metric("Differential Voltage", f"{abs(v_out_lvdt):.2f} V", delta=f"{'Positive Phase' if disp >=0 else 'Negative Phase'}")
        
        d_range = np.linspace(-20, 20, 40)
        v_range = d_range * 0.25
        fig3 = go.Figure(go.Scatter(x=d_range, y=v_range, line=dict(color='purple', width=4)))
        fig3.add_vline(x=0, line_dash="dash", line_color="black")
        fig3.update_layout(title="LVDT Linearity Curve", xaxis_title="Displacement (mm)", yaxis_title="Output Voltage (V)")
        st.plotly_chart(fig3)

    with t3:
        if st.button("Finalize LVDT Lab"):
             st.balloons()
