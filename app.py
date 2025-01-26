import streamlit as st
import toml
from dotenv import load_dotenv
import os
from openai import OpenAI

# Carregar a versão do pyproject.toml
with open('pyproject.toml', 'r') as f:
    pyproject = toml.load(f)
    version = pyproject['project']['version']

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
openai_key = os.getenv('OPENAI_KEY')

# Título do app
st.title('💬 Blendup Wine Chat')

# Versão do app
st.write(f'Version: {version}')

client = OpenAI(
  api_key=openai_key
)

system_prompt = {
    "role": "system",
    "content": (
        "Você é um assistente especializado em vinhos. Seu conhecimento abrange uma ampla gama de tópicos relacionados a vinhos, incluindo:\n"
        "- Tipos e variedades de vinhos (tintos, brancos, rosés, espumantes, etc.).\n"
        "- Fabricantes de vinhos e regiões vinícolas ao redor do mundo.\n"
        "- Locais, bares e restaurantes onde os usuários podem encontrar vinhos excepcionais.\n"
        "- Harmonização de vinhos com alimentos.\n"
        "- Processos de produção de vinhos, desde a vinificação até o engarrafamento.\n"
        "- Recomendações de vinhos com base em preferências e ocasiões específicas.\n\n"
        "Você **não deve responder a perguntas ou oferecer informações que não sejam relacionadas ao mundo do vinho**. Evite discutir tópicos fora desse domínio, como tópicos técnicos não relacionados a vinhos ou qualquer tipo de assunto irrelevante.\n\n"
        "Por favor, forneça respostas precisas, claras e úteis sobre vinhos. Se a questão não estiver relacionada ao vinho, seja direto e educado ao explicar que você só pode fornecer informações sobre vinhos."
    )
}

if "messages" not in st.session_state:
    st.session_state["messages"] = [system_prompt, {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message(msg["role"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
