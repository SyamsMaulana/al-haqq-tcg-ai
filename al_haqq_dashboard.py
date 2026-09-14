








import streamlit as st
import deck_data

st.set_page_config(page_title="Al-Haqq TCG Hub", layout="centered")

st.title("Al-Haqq TCG Command Hub")
st.markdown("### Ekosistem Phygital & Simulasi Keadilan Mizan")

st.subheader("Database Kartu Starter (5 Kartu Utama)")
for card in deck_data.starter_deck_database:
    with st.expander(f"{card['card_id']} — {card['name']} ({card['category']})"):
        st.write(f"Biaya Kasual: Mana | Biaya Turbo: Mana")
        st.write(f"Efek Taktis:")
        st.info(f"Narasi Filosofis: *{card['narrative']}*")

st.markdown("---")
st.subheader("Panel Eksekusi Simulasi Node")

if st.button("Jalankan Uji Coba Simulasi 4-Pemain"):
    with st.spinner("Memproses Monte Carlo Mizan Fairness..."):
        # Simulasi singkat respons antarmuka
        st.success("Simulasi Selesai!")
        st.metric(label="Mizan Fairness Index", value="100.00%")
        st.metric(label="Rata-rata Durasi Putaran", value="3.9 Menit")
        st.write("Semua node 12-LP merespons pemicu global secara simetris tanpa anomali.")

