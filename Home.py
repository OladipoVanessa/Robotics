import streamlit as st

st.set_page_config(page_title="CSI Robotics Assistant", layout="wide")

st.title("🤖 CSI Robotics Diagnostics Assistant")
st.write("""
Welcome to the Robotics Collision Diagnostics System.

Use the sidebar to navigate:
- **Event Browser:** Explore structured robot events  
- **Diagnostics:** View torque, sensor, and alert context  
- **AI Maintenance Assistant:** Generate fix recommendations  
""")
