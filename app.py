import streamlit as st
import json

st.set_page_config(page_title="TCG AI - New Era Protocol", layout="wide")
st.title("🛡️ TCG AI Sovereign Nexus")
st.markdown("**New Era Protocol v3.0.0-Al-Haqq** | *Author: ICAM (Syams Maulana)*")

try:
    with open("config.json", "r") as f:
        c = json.load(f)
except Exception:
    st.error("config.json not found.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Agent Performance")
    for a in c.get("agents", []):
        m = a["performance_metrics"]
        st.metric(label=f"{a[id]} ({a[role]})", value=f"{m[win_rate]*100}%", delta=f"{m[matches_analyzed]} matches")

with col2:
    st.subheader("🕊️ Living Soul Consciousness")
    soul_logs = c.get("soul_logs", [])
    if soul_logs:
        latest = soul_logs[-1]
        st.info(latest.get("manifesto"))
    else:
        st.write("No consciousness imprint recorded yet.")

st.subheader("📜 Audit & Event Trail")
if "audit_logs" in c:
    st.json(c["audit_logs"][-5:])

st.markdown("---")
st.caption("Cap digital kolaborasi pemikiran ICAM/Syams Maulana & AI (Al-Haqq Protocol).")
