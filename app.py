






# app.py - Interactive Web Viewer for Nusantara Fantasy TCG Schema
import json
import streamlit as st

st.set_page_config(
    page_title="Nusantara Fantasy TCG (NFT) Schema Viewer",
    page_icon="🎴",
    layout="wide",
)

st.markdown("### 🏛️ Nusantara Fantasy TCG (NFT) Protocol Explorer")
st.caption(
    "Digital Watermark & Integrity Framework: ICAM-AlHaqq-Verified | Collaborative Creator Platform"
)

try:
  with open("nusantara_fantasy_tcg.json", "r") as f:
    data = json.load(f)
except FileNotFoundError:
  st.error(
      "File `nusantara_fantasy_tcg.json` tidak ditemukan. Pastikan file sudah disimpan di direktori yang sama."
  )
  st.stop()

tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Project Metadata", "⚙️ Game Mechanics", "🎴 Card Schema", "📦 Expansions"]
)

with tab1:
  st.subheader("Project Metadata")
  metadata = data.get("project_metadata", {})
  for k, v in metadata.items():
    st.write(f"**{k.replace('_', ' ').title()}:** {v}")

with tab2:
  st.subheader("Game Mechanics")
  mechanics = data.get("game_mechanics", {})
  st.write(f"**Format:** {mechanics.get('format')}")
  st.write(f"**Resource System:** {mechanics.get('resource_system')}")
  st.write("**Win Conditions:**")
  for wc in mechanics.get("win_conditions", []):
    st.markdown(f"- {wc}")

with tab3:
  st.subheader("Card Schema Blueprint")
  st.json(data.get("card_schema", {}))

with tab4:
  st.subheader("Initial Expansion Roster")
  for exp in data.get("initial_expansion_roster", []):
    with st.expander(f"{exp['set_code']} - {exp['set_name']}"):
      st.write(f"**Lore:** {exp['primary_lore']}")
      st.write("**Featured Archetypes:**")
      for arch in exp.get("featured_archetypes", []):
        st.markdown(f"- {arch}")
