import streamlit as st
import pandas as pd

st.title("📁 Event Browser")

@st.cache_data
def load_data():
    return pd.read_csv("collision_events_master.csv")

df = load_data()

st.subheader("Filter Events")

severity = st.multiselect("Severity", df["severity"].unique())
ctype = st.multiselect("Collision Type", df["collision_type"].unique())
joint = st.multiselect("Joint", df["location_joint"].unique())

filtered = df.copy()

if severity:
    filtered = filtered[filtered["severity"].isin(severity)]
if ctype:
    filtered = filtered[filtered["collision_type"].isin(ctype)]
if joint:
    filtered = filtered[filtered["location_joint"].isin(joint)]

st.dataframe(filtered, use_container_width=True)

st.subheader("Select an Event")
selected_id = st.selectbox("Record ID", filtered["record_id"].tolist())

event = df[df["record_id"] == selected_id].iloc[0]

st.write("### Event Details")
st.json(event.to_dict())

st.session_state["selected_event"] = event.to_dict()
