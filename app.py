import streamlit as st

st.set_page_config(
    page_title="CSI Collision Intelligence Tool",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CSI Collision Intelligence Assistant")

st.markdown("""
This tool demonstrates how we:

1. **Structure messy robot collision data** into a clean schema.
2. **Browse and filter collision events** in an operator-friendly view.
3. **Generate technician-ready maintenance recommendations** from the structured data.

Use the sidebar to navigate:

- **Upload & Process** – load or replace the structured collision dataset.
- **Structured Data** – filter and explore collision events.
- **Diagnostics** – view summaries and severity patterns.
- **AI Assistant** – get maintenance recommendations for a selected event.
""")
