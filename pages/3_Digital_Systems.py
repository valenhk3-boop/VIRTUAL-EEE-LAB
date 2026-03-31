import streamlit as st
import pandas as pd
from utils.pdf_handler import generate_report
from datetime import datetime

if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Please login on the Homepage.")
    st.stop()

st.title("🔢 Digital Systems Design Lab")

exp = st.sidebar.radio("Select Experiment", [
    "1. Verification of Logic Gates",
    "2. Half Adder & Full Adder",
    "3. 4:1 Multiplexer (MUX)"
])

# --- EXPERIMENT 1: LOGIC GATES ---
if exp == "1. Verification of Logic Gates":
    st.header("Ex 1: Verification of Logic Gates")
    t1, t2, t3 = st.tabs(["📖 Manual", "🕹️ Workbench", "📝 Record"])
    
    with t1:
        st.subheader("Aim")
        st.write("To verify the truth tables of various logic gates (AND, OR, NOT, NAND, NOR, XOR).")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Logic-gates.svg/500px-Logic-gates.svg.png")
        st.subheader("Procedure")
        st.write("1. Select a gate. 2. Toggle inputs A and B. 3. Observe the LED output. 4. Verify with the Truth Table.")

    with t2:
        gate_type = st.selectbox("Select Gate to Test", ["AND", "OR", "NAND", "NOR", "XOR"])
        c1, c2 = st.columns(2)
        with c1:
            a = st.toggle("Input A")
            b = st.toggle("Input B")
        
        # Logic Solver
        if gate_type == "AND": res = int(a and b)
        elif gate_type == "OR": res = int(a or b)
        elif gate_type == "NAND": res = int(not(a and b))
        elif gate_type == "NOR": res = int(not(a or b))
        elif gate_type == "XOR": res = int(a ^ b)

        with c2:
            st.markdown(f"### Output Y: ` {res} `")
            st.progress(res * 100) # Simple visual "LED"

    with t3:
        if st.button("Generate Gate Report"):
            st.session_state.completed_labs["Logic Gates"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
            pdf = generate_report(st.session_state.user, "3.1 Logic Gates", "To verify truth tables.", "Toggle switches and verify.", f"Gate Tested: {gate_type}. Verification Successful.")
            st.download_button("Download Report", data=pdf, file_name="Logic_Gates.pdf")

# --- EXPERIMENT 2: ADDERS ---
elif exp == "2. Half Adder & Full Adder":
    st.header("Ex 2: Half Adder and Full Adder Design")
    t1, t2, t3 = st.tabs(["📖 Manual", "🕹️ Workbench", "📝 Record"])
    
    with t1:
        st.write("**Aim:** To design and verify the logic of Half and Full Adders.")
        
        st.latex(r"Sum = A \oplus B \oplus Cin")
        st.latex(r"Carry = (A \cdot B) + (Cin \cdot (A \oplus B))")

    with t2:
        mode = st.radio("Type", ["Half Adder", "Full Adder"])
        col1, col2, col3 = st.columns(3)
        A = col1.toggle("A")
        B = col2.toggle("B")
        Cin = col3.toggle("Cin") if mode == "Full Adder" else 0
        
        if mode == "Half Adder":
            S, C = (A ^ B), (A and B)
        else:
            S = (A ^ B ^ Cin)
            C = (A and B) or (Cin and (A ^ B))
            
        st.metric("SUM", int(S))
        st.metric("CARRY", int(C))

    with t3:
        if st.button("Export Adder Report"):
            pdf = generate_report(st.session_state.user, "3.2 Adders", "Verify Sum and Carry.", "Logic gate assembly.", "Verified Half and Full Adder logic.")
            st.download_button("Download PDF", data=pdf, file_name="Adders.pdf")

# --- EXPERIMENT 3: MUX ---
elif exp == "3. 4:1 Multiplexer (MUX)":
    st.header("Ex 3: 4:1 Multiplexer Verification")
    t1, t2, t3 = st.tabs(["📖 Manual", "🕹️ Workbench", "📝 Record"])
    with t1:
        st.write("**Aim:** To verify the functional table of a 4-to-1 Multiplexer.")
        
    with t2:
        s1 = st.checkbox("Select S1")
        s0 = st.checkbox("Select S0")
        inputs = [st.toggle(f"Data Input D{i}") for i in range(4)]
        
        sel = (int(s1) << 1) | int(s0)
        output = int(inputs[sel])
        st.success(f"Selected Input: D{sel} | Output Y: {output}")
    with t3:
        if st.button("Export MUX Report"):
             st.session_state.completed_labs["MUX"] = {"date": datetime.now().strftime("%Y-%m-%d"), "score": 100}
             st.write("Ready for download.")
