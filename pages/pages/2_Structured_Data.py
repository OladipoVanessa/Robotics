import streamlit as st
import pandas as pd

st.title("📁 Structured Collision Events")

df = st.session_state.get("df_master")

if df is None:
    st.error("No structured data found. Please go to **Upload & Process** first.")
    st.stop()

st.markdown("Use the filters below to explore collision events.")

# Defensive: make sure expected columns exist
expected_cols = [
    "record_id", "timestamp_iso", "collision_type", "location_joint",
    "severity", "torque_peak_pct", "force_value", "status"
]
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    st.warning(f"Some expected columns are missing: {missing}. The table will still display available fields.")

# Filters (guard against missing)
severity_options = df["severity"].dropna().unique() if "severity" in df.columns else []
collision_options = df["collision_type"].dropna().unique() if "collision_type" in df.columns else []
joint_options = df["location_joint"].dropna().unique() if "location_joint" in df.columns else []

col1, col2, col3 = st.columns(3)
with col1:
    severity = st.multiselect("Severity", sorted(severity_options))
with col2:
    ctype = st.multiselect("Collision Type", sorted(collision_options))
with col3:
    joint = st.multiselect("Joint", sorted(joint_options))

filtered = df.copy()

if severity and "severity" in filtered.columns:
    filtered = filtered[filtered["severity"].isin(severity)]
if ctype and "collision_type" in filtered.columns:
    filtered = filtered[filtered["collision_type"].isin(ctype)]
if joint and "location_joint" in filtered.columns:
    filtered = filtered[filtered["location_joint"].isin(joint)]

st.subheader(f"Filtered Events ({len(filtered)} records)")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "⬇️ Download filtered events as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_collision_events.csv",
    mime="text/csv"
)

if "record_id" in filtered.columns and len(filtered) > 0:
    st.subheader("Inspect a Single Event")
    selected_id = st.selectbox("Select record_id", filtered["record_id"].tolist())

    event = df[df["record_id"] == selected_id].iloc[0].to_dict()
    st.json(event)
else:
    st.info("No records available to inspect.")
