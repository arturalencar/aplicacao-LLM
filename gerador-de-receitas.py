import streamlit as st
from google import genai
import os
from dataclasses import dataclass

@dataclass
class ModelConfig:
    provider: str = "google"
    model_name: str = "gemini-2.5-flash" 
    temperature: float = 0.7             # Nível de criatividade
    max_tokens: int = 1000000            # Tamanho máximo da receita
    modality: str = "text"              

st.title("Gerador de Receitas com Restrições")

config = ModelConfig()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

receita = st.text_input("Qual receita você deseja fazer?")
alergias = st.text_input("Quais são suas alergias?")

for model in client.models.list():
    print(model.name)

if st.button("Gerar Receita"):
    entrada = (
        f"Eu gostaria de fazer uma receita de {receita}. "
        f"Eu tenho as seguintes alergias: {alergias}. "
        "Envie-me a receita que atende ao meu desejo e às minhas alergias."
    )

    response = client.models.generate_content(
        model=config.model_name,
        contents=entrada,
        config={
            'max_output_tokens': config.max_tokens,
            'temperature': config.temperature,
        }
    )

    st.subheader("Receita sugerida:")
    st.write(response.text)