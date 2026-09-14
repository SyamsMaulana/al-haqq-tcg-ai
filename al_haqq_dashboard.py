










# al_haqq_dashboard.py — Streamlit Command Hub Dashboard (Versi Anti-Pyarrow)
import streamlit as st
import json
import os
from phygital_verifier import PhygitalVerifier
from deck_builder import DeckBuilder

st.set_page_config(
    page_title="Al-Haqq Protocol Command Hub",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Al-Haqq Protocol TCG — Command Hub")
st.markdown("*Integritas Al-Haqq Framework & Karsa Kreatif Kolektif*")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Phygital Verifier", 
    "🃏 Mizan Deck Builder", 
    "🏆 Tournament Standings", 
    "📖 Rulebook & Docs"
])

with tab1:
    st.subheader("Verifikasi Kriptografis Aset Phygital (QR/NFC)")
    verifier = PhygitalVerifier()
    input_hash = st.text_input("Masukkan Token/Hash Verifikasi:", "ALHAQQ-VERIFIED-")
    if st.button("Verifikasi Token"):
        result = verifier.verify_token(input_hash)
        if result["status"] == "AUTENTIK":
            st.success(f"Status: {result['status']}")
            st.json(result)
        else:
            st.error(f"Status: {result['status']}")

with tab2:
    st.subheader("Pembangunan & Validasi Dek Berbasis Mizan")
    builder = DeckBuilder()
    selected_card = st.text_input("Masukkan Card ID (contoh: AH-001, AG-001):", "AH-001")
    if st.button("Tambah ke Dek"):
        success, msg = builder.add_card_to_deck(selected_card)
        if success:
            st.success(msg)
        else:
            st.warning(msg)
    
    report = builder.validate_mizan_deck()
    st.markdown(f"**Total Kartu:** {report['total_cards']} / 15")
    st.markdown(f"**Status Mizan:** {report['mizan_status']}")
    st.write("Isi Dek Saat Ini:")
    st.json(report['deck_contents'])

with tab3:
    st.subheader("Papan Peringkat Turnamen G.O.D TCG")
    if os.path.exists("tournament_standings.json"):
        with open("tournament_standings.json", "r", encoding="utf-8") as f:
            standings_data = json.load(f)
        st.json(standings_data)
    else:
        st.info("Belum ada data turnamen. Jalankan tournament_manager.py terlebih dahulu.")

with tab4:
    st.subheader("Buku Panduan Resmi (Rulebook)")
    if os.path.exists("AL_HAQQ_RULEBOOK.md"):
        with open("AL_HAQQ_RULEBOOK.md", "r", encoding="utf-8") as f:
            rulebook_content = f.read()
        st.markdown(rulebook_content)
    else:
        st.info("Rulebook belum di-generate.")
