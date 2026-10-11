import streamlit as st
import requests
from datetime import datetime, time

# Setări pagină
st.set_page_config(page_title="O întrebare importantă...", page_icon="💖", layout="centered")

# Stiluri vizuale
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .title-text { text-align: center; color: #ff4b4b; font-size: 2.5rem; font-weight: bold; }
    .subtitle-text { text-align: center; color: #31333F; font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# Stare sesiune
if "raspuns_confirmat" not in st.session_state:
    st.session_state.raspuns_confirmat = False

if "buton_nu_apasari" not in st.session_state:
    st.session_state.buton_nu_apasari = 0

if "status_trimis" not in st.session_state:
    st.session_state.status_trimis = None

# Titlu
st.markdown('<p class="title-text">Hei! Am o întrebare serioasă pentru tine... 🫵</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Vrei să ieșim la o întâlnire săptămâna asta? ☕✨</p>', unsafe_allow_html=True)

st.write("")
st.write("")

# Întrebarea
if not st.session_state.raspuns_confirmat:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🥰 DA, evident!", use_container_width=True):
            st.session_state.raspuns_confirmat = True
            st.rerun()

    with col2:
        mesaje_nu = [
            "Nu 😢", 
            "Sigur ești sigură?", 
            "Mai gândește-te!", 
            "Butonul ăsta e stricat 🤖", 
            "Nici o șansă să apeși aici!", 
            "Ia mai apasă o dată pe DA 😌"
        ]
        
        text_nu_curent = mesaje_nu[min(st.session_state.buton_nu_apasari, len(mesaje_nu) - 1)]
        
        if st.button(text_nu_curent, use_container_width=True):
            st.session_state.buton_nu_apasari += 1
            st.rerun()
            
    if st.session_state.buton_nu_apasari > 0:
        st.info("💡 Hint: Sistemul a detectat că butonul de 'Nu' nu funcționează corect. Singura opțiune validă a rămas cea stângă! 😇")

# Formularul după ce se apasă pe DA
else:
    st.balloons()
    st.success("Yuhuu! Știam eu! 🎉 Acum, partea logistică:")

    st.subheader("🗓️ Alege data și ora care îți convin:")
    
    ziua_aleasa = st.date_input("În ce zi ne vedem?", min_value=datetime.today())
    ora_aleasa = st.time_input("La ce oră?", value=time(18, 0))

    locatie_aleasa = st.selectbox(
        "Unde mergem?",
        ["☕ O cafenea drăguță în oraș", "🍰 La o prăjitură bună", "🧋 Bubble tea", "🚶‍♂️ O plimbare în parc"]
    )

    if st.button("Confirmă Întâlnirea 🚀", use_container_width=True):
        data_str = ziua_aleasa.strftime('%A, %d %B %Y')
        ora_str = ora_aleasa.strftime('%H:%M')
        
        ACCESS_KEY = "62b6c96a-963f-471f-9722-4750bb1bdf63"
        
        payload = {
            "access_key": ACCESS_KEY,
            "subject": "🎉 Ioana a confirmat întâlnirea!",
            "message": f"Ioana a ales:\n- Data: {data_str}\n- Ora: {ora_str}\n- Locația: {locatie_aleasa}"
        }
        
        try:
            rezultat = requests.post("https://api.web3forms.com/submit", data=payload)
            st.session_state.status_trimis = rezultat.json()
        except Exception as e:
            st.session_state.status_trimis = {"success": False, "message": str(e)}

    # Afișăm statusul permanent dacă a fost trimis
    if st.session_state.status_trimis:
        if st.session_state.status_trimis.get("success"):
            st.success("✅ E-mailul a fost trimis cu succes către tine!")
        else:
            st.error(f"❌ Erore la trimitere: {st.session_state.status_trimis}")

    st.markdown(f"""
    ### E oficial! 🥳
    - **Data:** {data_str}
    - **Ora:** {ora_str}
    - **Locația:** {locatie_aleasa}
    
    *Abia aștept! O să fie super tare.* ✨
    """)
