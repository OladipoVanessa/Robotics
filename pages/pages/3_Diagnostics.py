import streamlit as st
import pandas as pd

st.title("📊 Diagnostics & Patterns")

df = st.session_state.get("df_master")

if df is None:
    st.error("No structured data found. Please go to **Upload & Process** first.")
    st.stop()

st.markdown("""
This page summarizes collision patterns across joints, severity levels, and torque peaks.
Use this to explain **how your structured schema supports analysis and maintenance planning**.
""")

col1, col2, col3 = st.columns(3)

with col1:
    if "severity" in df.columns:
        st.subheader("Counts by Severity")
        st.dataframe(df["severity"].value_counts().rename_axis("severity").reset_index(name="count"))
    else:
        st.info("No `severity` column found.")

with col2:
    if "location_joint" in df.columns:
        st.subheader("Counts by Joint")
        st.dataframe(df["location_joint"].value_counts().rename_axis("joint").reset_index(name="count"))
    else:
        st.info("No `location_joint` column found.")

with col3:
    if "collision_type" in df.columns:
        st.subheader("Counts by Collision Type")
        st.dataframe(df["collision_type"].value_counts().rename_axis("type").reset_index(name="count"))
    else:
        st.info("No `collision_type` column found.")

st.markdown("---")

if "torque_peak_pct" in df.columns:
    st.subheader("Torque Peak Summary")
    st.write(df["torque_peak_pct"].describe())
else:
    st.info("No `torque_peak_pct` column found to summarize.")
