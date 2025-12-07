import streamlit as st
import pandas as pd

st.title("🧠 AI Maintenance Assistant")

df = st.session_state.get("df_master")

if df is None:
    st.error("No structured data found. Please go to **Upload & Process** first.")
    st.stop()

required_cols = ["record_id", "severity", "collision_type", "location_joint", "torque_peak_pct", "force_value"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.warning(f"Some expected columns are missing: {missing}. The assistant will use what is available.")

st.markdown("""
Select a collision event and the assistant will generate **recommended actions and procedure steps**
based on the event's severity, joint location, and torque/force profile.
""")

record_ids = df["record_id"].tolist() if "record_id" in df.columns else list(df.index)
selected = st.selectbox("Select an event", record_ids)

if "record_id" in df.columns:
    event = df[df["record_id"] == selected].iloc[0].to_dict()
else:
    event = df.loc[selected].to_dict()

def generate_recommendation(ev: dict) -> dict:
    severity = ev.get("severity", "unknown")
    joint = ev.get("location_joint", "unknown joint")
    ctype = ev.get("collision_type", "collision")
    torque = ev.get("torque_peak_pct", None)
    force = ev.get("force_value", None)

    title = ""
    summary = ""
    steps = []

    # Basic severity-driven logic
    if severity == "critical":
        title = "Immediate Lockout and Detailed Inspection"
        summary = (
            f"Critical {ctype} detected near {joint}. Robot should remain locked out until "
            "full mechanical and electrical inspection is completed."
        )
        steps = [
            "1. Engage lockout/tagout on the robot controller.",
            f"2. Visually inspect {joint} for deformation, loose fasteners, and abnormal noise.",
            "3. Check reducer and motor shaft for binding or excessive backlash.",
            "4. Run encoder alignment and position calibration routines.",
            "5. After mechanical checks, execute a slow-speed dry run of the last program segment.",
            "6. Document findings and update maintenance log before returning robot to service."
        ]
    elif severity == "high":
        title = "Priority Inspection and Recalibration"
        summary = (
            f"High-severity {ctype} detected. Robot can remain powered but should not resume production "
            "until a focused inspection is done."
        )
        steps = [
            "1. Inspect the affected joint area for impact marks and loose mounting hardware.",
            "2. Verify reducer and encoder alignment for that axis.",
            "3. Review recent torque and vibration trends around the event timestamp.",
            "4. Recalibrate joint positions if deviations are found.",
            "5. Run a supervised test cycle at reduced speed."
        ]
    elif severity == "medium":
        title = "Scheduled Inspection and Monitoring"
        summary = (
            "Medium-severity event detected. No immediate shutdown required, but the joint should be "
            "scheduled for inspection and monitored for repeat patterns."
        )
        steps = [
            "1. Check historical torque and vibration patterns for this joint.",
            "2. Inspect harnessing, fixtures, and surrounding workspace for intermittent interference.",
            "3. Add this joint to the next scheduled maintenance round.",
            "4. Configure alerts if torque exceeds defined thresholds in upcoming cycles."
        ]
    else:
        title = "Log-Only Event with Monitoring"
        summary = (
            "Low-severity or unclassified event. Record the event and continue operation with light monitoring."
        )
        steps = [
            "1. Log the event details in the maintenance system.",
            "2. Monitor for repeated events at the same joint or program step.",
            "3. Escalate if frequency or intensity increases over time."
        ]

    # Enrich with data references if available
    details = []
    if torque is not None:
        details.append(f"- Peak torque near event: **{torque:.1f}% of rated**")
    if force is not None:
        details.append(f"- Representative force/vibration metric: **{force:.3f}**")

    return {
        "title": title,
        "summary": summary,
        "details": "\n".join(details),
        "steps": steps
    }

if st.button("Generate Recommendation"):
    rec = generate_recommendation(event)

    st.subheader(rec["title"])
    st.write(rec["summary"])

    if rec["details"]:
        st.markdown("**Event context:**")
        st.markdown(rec["details"])

    st.markdown("**Procedure steps:**")
    for step in rec["steps"]:
        st.write(step)
