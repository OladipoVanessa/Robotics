import streamlit as st
import pandas as pd

st.title("🧰 Diagnostics Panel")

if "selected_event" not in st.session_state:
    st.warning("Please select an event from the Event Browser first.")
    st.stop()

event = st.session_state["selected_event"]

st.subheader(f"Event: {event['record_id']}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Collision Type", event["collision_type"])
    st.metric("Joint", event["location_joint"])
    st.metric("Severity", event["severity"])

with col2:
    st.metric("Peak Torque (%)", event["torque_peak_pct"])
    st.metric("Force Value", event["force_value"])

st.write("### Error Codes")
st.write(event["error_codes"])

st.write("### Alerts")
st.write(event["alert_type"])

st.write("### Maintenance Notes")
st.write(event["maintenance_notes"] if event["maintenance_notes"] else "No notes")
