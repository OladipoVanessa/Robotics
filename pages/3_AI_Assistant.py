import streamlit as st

st.title("🧠 AI Maintenance Assistant")

if "selected_event" not in st.session_state:
    st.warning("Please select an event from the Event Browser first.")
    st.stop()

event = st.session_state["selected_event"]

st.subheader(f"Generate recommendations for: {event['record_id']}")

def basic_ai(event):
    if event["collision_type"] == "hard_collision":
        return {
            "action": "Immediate shutdown & physical inspection",
            "steps": [
                "Power off the robot",
                "Verify joint alignment",
                "Inspect cables and gears",
                "Run servo diagnostics",
            ],
            "confidence": "0.92"
        }
    elif event["collision_type"] == "soft_collision":
        return {
            "action": "Review torque thresholds",
            "steps": [
                "Check for gradual drift",
                "Inspect joint lubrication",
                "Lower speed in high-risk cycles",
            ],
            "confidence": "0.78"
        }
    else:
        return {
            "action": "Monitor and schedule maintenance",
            "steps": [
                "Review logs over next 10 cycles",
                "Check sensor drift",
                "Run system health test",
            ],
            "confidence": "0.66"
        }

response = basic_ai(event)

st.write("### Recommended Action")
st.success(response["action"])

st.write("### Procedure Steps")
for step in response["steps"]:
    st.write(f"- {step}")

st.write("### Confidence Level")
st.metric("Confidence", response["confidence"])
