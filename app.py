





# app.py - Integrated Nusantara Fantasy TCG Portal (Fixed Quote Syntax)
import json
import os
import streamlit as st

st.set_page_config(
    page_title="Nusantara Fantasy TCG (NFT) Platform",
    page_icon="🎴",
    layout="wide",
)

st.markdown("### 🏛️ Nusantara Fantasy TCG (NFT) Protocol Explorer")
st.caption(
    "Digital Watermark & Integrity Framework: ICAM-AlHaqq-Verified |"
    " Collaborative Creator Platform"
)

try:
  with open("nusantara_fantasy_tcg.json", "r") as f:
    data = json.load(f)
except FileNotFoundError:
  data = {}

try:
  with open("cards.json", "r") as f:
    cards_data = json.load(f)
except FileNotFoundError:
  cards_data = []

tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Metadata & Mechanics", "🎴 Card Codex", "📜 Official Rulings", "🛡️ Watermark Utility"]
)

with tab1:
  st.subheader("Project Metadata")
  metadata = data.get("project_metadata", {})
  for k, v in metadata.items():
    st.write(f"**{k.replace('_', ' ').title()}:** {v}")

  st.subheader("Game Mechanics")
  mechanics = data.get("game_mechanics", {})
  st.write(f"**Format:** {mechanics.get('format')}")
  st.write(f"**Resource System:** {mechanics.get('resource_system')}")
  st.write("**Win Conditions:**")
  for wc in mechanics.get("win_conditions", []):
    st.markdown(f"- {wc}")

with tab2:
  st.subheader("Initial Expansion Card Codex")
  if cards_data:
    for card in cards_data:
      c_id = card["card_id"]
      c_name = card["card_name"]
      c_type = card["card_type"]
      affinity = card["elemental_affinity"]
      cost = card["resource_cost"]
      atk = card["attributes"]["attack_power"]
      dfn = card["attributes"]["defense_integrity"]
      rarity = card["digital_integrity"]["rarity_tier"]
      hsh = card["digital_integrity"]["hash_signature"]
      lore = card["lore_snippet"]

      with st.expander(f"{c_id} — {c_name} [{c_type}]"):
        col1, col2 = st.columns(2)
        with col1:
          st.write(f"**Affinity:** {affinity}")
          st.write(f"**Resource Cost:** {cost}")
          st.write(f"**Attack:** {atk}")
          st.write(f"**Defense:** {dfn}")
        with col2:
          st.write(f"**Rarity:** {rarity}")
          st.write(f"**Hash:** `{hsh}`")
        st.markdown(f"> *{lore}*")
  else:
    st.info("No card data found in `cards.json`.")

with tab3:
  st.subheader("Official Codex & Rulings")
  if os.path.exists("rulings.md"):
    with open("rulings.md", "r") as f:
      st.markdown(f.read())
  else:
    st.info("Rulings documentation not found.")

with tab4:
  st.subheader("Al-Haqq Digital Watermark Integration")
  st.write(
      "The watermark protocol ensures cryptographic integrity and authentic"
      " ownership attribution across all generated assets."
  )
  st.code(
      "python3 watermark_utility.py --input asset.png --output"
      " watermarked_asset.png --id NFT-HERO-001",
      language="bash",
  )




