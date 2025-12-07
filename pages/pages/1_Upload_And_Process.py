import streamlit as st
import pandas as pd

st.title("📤 Upload & Process Structured Data")

st.markdown("""
This page loads the **structured collision dataset** produced by your Python pipeline
(e.g., the `collision_events_master.csv` file generated from the raw FANUC logs).

On competition day, you can:
1. Run your Colab/Python pipeline on the new raw files.
2. Export `collision_events_master.csv`.
3. Upload that file here to refresh the app.
""")

uploaded_file = st.file_uploader(
    "Upload `collision_events_master.csv`",
    type=["csv"],
    help="This is the structured output from your data pipeline."
)

if "df_master" not in st.session_state:
    st.session_state["df_master"] = None

if uploaded_file is not None:
    df_master = pd.read_csv(uploaded_file)
    st.session_state["df_master"] = df_master
    st.success(f"Uploaded and loaded {uploaded_file.name} with {len(df_master)} records.")
else:
    # Try to load default CSV from repo
    try:
        df_master_default = pd.read_csv("collision_events_master.csv")
        st.session_state["df_master"] = df_master_default
        st.info(f"No upload detected. Using default `collision_events_master.csv` ({len(df_master_default)} records).")
    except FileNotFoundError:
        st.error(
            "No file uploaded and no default `collision_events_master.csv` found in the repo. "
            "Please upload a structured dataset to continue."
        )

if st.session_state["df_master"] is not None:
    st.subheader("Preview")
    st.dataframe(st.session_state["df_master"].head(), use_container_width=True)
    st.caption("Showing first 5 records of the structured dataset.")
