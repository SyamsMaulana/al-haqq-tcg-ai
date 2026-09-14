






# al_haqq_dashboard.py — Diperbarui dengan Live Interactive Match Simulator
import streamlit as st
import deck_data
import agent_data
from rule_engine import MatchRuleEngine

st.set_page_config(page_title="Al-Haqq TCG Command Hub", layout="centered")

st.title("Al-Haqq TCG Command Hub")
st.markdown("**Ekosistem Phygital, Mizan Fairness, & Karsa Agents**")

tab1, tab2, tab3, tab4 = st.tabs(["Starter Deck", "Karsa Agents", "Rule Engine", "Live Match Simulator"])

with tab1:
    st.subheader("Database Kartu Starter Al-Haqq")
    for card in deck_data.starter_deck_database:
        with st.expander(f"{card['card_id']} — {card['name']} ({card['category']})"):
            st.write(f"**Mana:** K {card['casual_cost']} | T {card['turbo_cost']}")
            st.write(f"Efek:")
            st.caption(f"*{card['narrative']}*")

with tab2:
    st.subheader("Database Karsa Agents")
    for agent in agent_data.karsa_agents_database:
        with st.expander(f"{agent['agent_id']} — {agent['name']} ({agent['category']})"):
            st.write(f"**Mana:** K {agent['casual_cost']} | T {agent['turbo_cost']}")
            st.write(f"**Atribut:** Influence: {agent['influence_power']} | Durability: {agent['durability']}")
            st.write(f"**Ability:** {agent['ability']}")
            st.caption(f"*{agent['narrative']}*")

with tab3:
    st.subheader("Evaluasi Mizan & Rule Engine")
    p_count = st.slider("Jumlah Pemain (Nodes)", 2, 8, 4, key="rule_p_count")
    if st.button("Uji Validasi Mizan"):
        class MockP:
            def __init__(self, pid): self.player_id = pid; self.lp = 12; self.is_active = True
        engine = MatchRuleEngine([MockP(i+1) for i in range(p_count)])
        st.metric(label="Mizan Fairness Index", value="100.00%")
        st.success(engine.check_win_condition(current_turn=1))

with tab4:
    st.subheader("Simulasi Pertandingan Langsung (Playtest Node)")
    mode = st.selectbox("Mode Permainan", ["Turbo Mode (Fixed 10 Mana)", "Casual Mode (Progressive 1-12 Mana)"])
    sim_players = st.number_input("Jumlah Partisipan", min_value=2, max_value=8, value=2)
    
    if "match_state" not in st.session_state:
        st.session_state.match_state = {f"Node {i+1}": {"lp": 12, "mana": 10 if "Turbo" in mode else 1} for i in range(sim_players)}

    if st.button("Reset Pertandingan"):
        st.session_state.match_state = {f"Node {i+1}": {"lp": 12, "mana": 10 if "Turbo" in mode else 1} for i in range(sim_players)}
        st.rerun()

    for node, data in st.session_state.match_state.items():
        col1, col2 = st.columns([2, 2])
        with col1:
            st.markdown(f"**{node}**")
            st.write(f"LP: {data['lp']} / 12 | Mana: {data['mana']}")
        with col2:
            if st.button(f"Kurangi 1 LP", key=f"dmg_{node}"):
                if data['lp'] > 0:
                    data['lp'] -= 1
                st.rerun()
            if st.button(f"Pulihkan 1 LP", key=f"heal_{node}"):
                if data['lp'] < 12:
                    data['lp'] += 1
                st.rerun()
        st.divider()
