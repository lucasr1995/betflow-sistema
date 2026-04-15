import streamlit as st
from supabase import create_client
import pandas as pd

# CONFIGURAÇÃO VISUAL SAAS
st.set_page_config(page_title="BetFlow Analytics PRO", layout="wide")

# CONEXÃO (Substitua pelas suas chaves do Supabase)
URL = "https://aprxchasopfdptotuycv.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwcnhjaGFzb3BmZHB0b3R1eWN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYyNjAxNTcsImV4cCI6MjA5MTgzNjE1N30.tCh9_2dnSI20bjowY6T7v4br0NeoudTje3fsMm25jUQ"
supabase = create_client(URL, KEY)

# CSS PROFISSIONAL DARK
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #101419; color: white; }
    .game-card { background: #1e252e; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
    .btn-bet { display: inline-block; padding: 8px 15px; border-radius: 5px; font-weight: bold; text-decoration: none; font-size: 12px; margin-right: 5px; color: white; }
    </style>
""", unsafe_allow_html=True)

# SISTEMA DE LOGIN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.title("🔐 BetFlow PRO | Acesso")
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if u == "admin" and p == "123":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Erro!")
    st.stop()

# INTERFACE PRINCIPAL
t1, t2 = st.tabs(["📊 Palpites & Hub", "💬 Fórum"])

with t1:
    res = supabase.table("palpites_ia").select("*").execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        for liga in df['liga'].unique():
            st.subheader(f"🏆 {liga}")
            jogos = df[df['liga'] == liga]
            c1, c2 = st.columns(2)
            for i, r in enumerate(jogos.itertuples()):
                with c1 if i % 2 == 0 else c2:
                    st.markdown(f"""
                    <div class="game-card">
                        <h3>{r.time_casa} × {r.time_fora}</h3>
                        <p style='color:#58a6ff;'>🎯 Dica IA: {r.conselho}</p>
                        <div style='margin-top:10px;'>
                            <a class="btn-bet" style="background:#f45b22;" href="https://br.betano.com/search?q={r.time_casa}">BETANO</a>
                            <a class="btn-bet" style="background:#e31c1c;" href="https://superbet.com/pt-br/search?query={r.time_casa}">SUPERBET</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

with t2:
    st.header("💬 Comunidade")
    # Exibe posts do fórum
    f_res = supabase.table("forum_posts").select("*").order("created_at", desc=True).execute()
    for p in f_res.data:
        st.write(f"**@{p['usuario']}**: {p['jogo']} -> {p['palpite']}")