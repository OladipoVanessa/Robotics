import streamlit as st
import pandas as pd

st.title("📤 Upload & Process Structured Data")

st.markdown("""
Upload your `collision_events_master.csv` file.  
If you don’t upload anything, the app will load the default file included in the repo.
""")

uploaded_file = st.file_uploader(
    "Upload your structured dataset",
    type=["csv"],
    help="Use the output of your Python pipeline"
)

if "df_master" not in st.session_state:
    st.session_state["df_master"] = None

if uploaded_file is not None:
    df_master = pd.read_csv(uploaded_file)
    st.session_state["df_master"] = df_master
    st.success(f"Loaded {len(df_master)} records from uploaded file.")
else:
    try:
        df_default = pd.read_csv("collision_events_master.csv")
        st.session_state["df_master"] = df_default
        st.info(f"Using default structured dataset ({len(df_default)} records).")
    except:
        st.warning("No file uploaded and no default CSV found. Please upload a file.")
