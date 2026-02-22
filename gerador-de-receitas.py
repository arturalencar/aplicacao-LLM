import streamlit as st
from google import genai
import os

st.title("Gerador de Receitas com Restrições")

# Cria o client UMA VEZ no início
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

receita = st.text_input("Qual receita você deseja fazer?")
alergias = st.text_input("Quais são suas alergias?")

if st.button("Gerar Receita"):

    entrada = (
        f"Eu gostaria de fazer uma receita de {receita}. "
        f"Eu tenho as seguintes alergias: {alergias}. "
        "Envie-me a receita que atende ao meu desejo e às minhas alergias."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=entrada
    )

    st.subheader("Receita sugerida:")
    st.write(response.text)