import requests
import streamlit as st
import pandas as pd

st.title("Consulta de CEP")

cep = st.sidebar.text_input("Digite o CEP", icon="🔎")

if st.sidebar.button("Pesquisar"):

    if not cep.isdigit() or len(cep) != 8:
        st.error("CEP inválido! Digite apenas 8 números.")
        st.stop()

    try:
        busca = requests.get(
            f"https://cep.awesomeapi.com.br/json/{cep}",
            timeout=5
        )
        busca.raise_for_status()
        busca = busca.json()

    except requests.exceptions.RequestException:
        st.error("Erro ao acessar a API.")
        st.stop()

    if "error" in busca:
        st.error("CEP não encontrado.")
        st.stop()

    st.subheader("📍 Endereço")

    st.write(f"**CEP:** {busca['cep']}")
    st.write(f"**Endereço:** {busca['address']}")
    st.write(f"**Bairro:** {busca['district']}")
    st.write(f"**Cidade:** {busca['city']}")
    st.write(f"**Estado:** {busca['state']}")
    st.write(f"**Latitude:** {busca['lat']}")
    st.write(f"**Longitude:** {busca['lng']}")

    try:
        mapa = pd.DataFrame({
            "lat": [float(busca["lat"])],
            "lon": [float(busca["lng"])]
        })

        st.subheader("🗺️ Localização")
        st.map(mapa)

    except (KeyError, ValueError):
        st.warning("Não foi possível exibir a localização no mapa.")