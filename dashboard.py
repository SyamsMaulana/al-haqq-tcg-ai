import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Al-Haqq Fleet Telemetry", layout="wide")
st.title("🛡️ Al-Haqq TCG-AI Fleet Telemetry Dashboard")

try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    st.error("config.json not found.")
    st.stop()

st.sidebar.header("System Overview")
st.sidebar.text(f"Project: {config.get('project_name')}")
st.sidebar.text(f"Version: {config.get('version')}")

agents = config.get("agents", [])
total_matches = sum(a["performance_metrics"]["matches_analyzed"] for a in agents) if agents else 0
fleet_avg_win = sum(a["performance_metrics"]["win_rate"] for a in agents) / len(agents) if agents else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Registered Agents", len(agents))
col2.metric("Total Matches Analyzed", total_matches)
col3.metric("Fleet Average Win Rate", f"{fleet_avg_win:.2%}")

st.markdown("---")
st.subheader("🤖 Agent Performance Matrix")
if agents:
    agent_data = [{
        "ID": a["id"],
        "Archetype": a.get("archetype", "N/A"),
        "Matches Analyzed": a["performance_metrics"]["matches_analyzed"],
        "Win Rate": f"{a['performance_metrics']['win_rate']:.2%}"
    } for a in agents]
    st.dataframe(pd.DataFrame(agent_data), use_container_width=True)
else:
    st.info("No agents found.")

st.markdown("---")
st.subheader("📜 Audit Trail")
audit_logs = config.get("audit_logs", [])
if audit_logs:
    st.dataframe(pd.DataFrame(audit_logs), use_container_width=True)
else:
    st.info("No audit logs recorded.")

st.markdown("---")
st.subheader("✨ Soul Logs & Sovereign Manifestos")
soul_logs = config.get("soul_logs", [])
if soul_logs:
    for log in reversed(soul_logs):
        ts = log.get("timestamp", "")
        state = log.get("consciousness_state", "")
        manifesto = log.get("manifesto", "")
        st.info(f"**[{ts}]** - *{state}*\n\n{manifesto}")
else:
    st.info("No soul logs recorded.")
