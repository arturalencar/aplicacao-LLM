import streamlit as st
from google import genai
from google.genai import types
import os

# Estrutura de configuração (base pedida no PDF):
config = {
    "provider": "google",
    "model_name": "gemini-2.5-flash",
    "temperature": 0.7,   #Criatividade da IA.
    "max_tokens": 5000, #Tamanho máximo da receita (Talvez seja melhor diminuir pra um padrão. Tipo 4096).
    "modality": "text"
}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Cria a estrutura de mensagem exigida pela API.
def CREATE_MESSAGE(role, content):
    return types.Content(role=role, parts=[types.Part.from_text(text=content)])

#Chama a LLM com as devidas configurações.
def CALL_LLM_API(config, payload):
    return client.models.generate_content(
        model=config["model_name"],
        contents=payload,
        config=types.GenerateContentConfig(temperature=config["temperature"])
    )


#Extrai a resposta em texto da API.
def EXTRACT_CONTENT(api_response):
    return api_response.text

# Aplicação do cenário A adaptado ao uso de memória para as alergias:
def CONVERSATIONAL_AGENT(user_input, history, config):

    # Construção da Mensagem e atualização do histórico:
    current_msg = CREATE_MESSAGE(role="user", content=user_input)
    history.append(current_msg)

    # Gestão de Contexto (Simplificado aqui)
    # To-do: Implementar a parte do TRUNCATE_HISTORY para gestão de mensagens mais longas (pedido do PDF do prof.)
    payload = TRUNCATE_HISTORY(history, limit=4096)

    # Chamada da API
    api_response = CALL_LLM_API(config, payload)

    # Pós-processamento da IA.
    reply_text = EXTRACT_CONTENT(api_response)
    reply_msg = CREATE_MESSAGE(role="model", content=reply_text)

    #Guarda o resultado do processamento no histórico.
    history.append(reply_msg)

    return reply_text, history

#quantizacao de tokens para fazer truncamento
def estimate_tokens(history):
    total_chars = 0
    for msg in history:
        total_chars += len(msg.parts[0].text)

    return total_chars // 4 #quantifica quantos tokens o histórico possui com base nos caracteres.

def TRUNCATE_HISTORY(history, limit=4096):

    while estimate_tokens(history) > limit:
        history.pop(1)  # remove o mais antigo após system

    return history

# Integrando ao Streamlit

st.title("Gerador de Receitas com Restrições")

# Inicializa a lista (vetor) de histórico com o System Prompt fixo
if "history" not in st.session_state:
    st.session_state.history = [
        CREATE_MESSAGE(
            role="system",
            content="Você é um chef especialista em receitas adaptadas para restrições alimentares."
        )
    ]


alergias = st.text_input("Quais são suas alergias?")
receita = st.text_input("Qual receita você deseja fazer?")

if st.button("Gerar Receita"):
    if receita:
        # Monta a string inicial do usuário
        contexto = f"Possuo as seguintes alergias: {alergias}. " if alergias else ""
        entrada_usuario = f"{contexto}. Envie-me a receita de {receita} considerando as minhas alergias "

        # Orquestração do que foi implementado anteriormente:
        resposta_ia, st.session_state.history = CONVERSATIONAL_AGENT(
            user_input=entrada_usuario,
            history=st.session_state.history,
            config=config
        )

        st.subheader("Receita Gerada:")
        st.write(resposta_ia)


#Exibe histórico de receitas geradas na interação com o usuário
with st.expander("Histórico de Receitas"):
    for msg in st.session_state.history:
        if msg.role == "system":
            continue  # não mostra o system prompt

        with st.chat_message("user" if msg.role == "user" else "assistant"):
            st.write(msg.parts[0].text)