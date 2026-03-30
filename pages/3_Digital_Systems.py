import streamlit as st

st.title("Digital Logic Lab")
gate = st.selectbox("Select Logic Gate", ["AND", "OR", "NAND", "NOR", "XOR"])

a = st.checkbox("Input A")
b = st.checkbox("Input B")

if gate == "AND": res = int(a and b)
elif gate == "OR": res = int(a or b)
elif gate == "NAND": res = int(not(a and b))
elif gate == "NOR": res = int(not(a or b))
elif gate == "XOR": res = int(a ^ b)

st.header(f"Output: {res}")
st.lottie = "✨" # Placeholder for animation
