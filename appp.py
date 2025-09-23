import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import random  # Usado para embaralhar

st.set_page_config(page_title="🎬 Quiz Netflix com Imagens", layout="centered")

st.title("🎬 Quiz Netflix com Imagens")
st.write("Teste seus conhecimentos sobre séries e filmes da Netflix! Olhe a imagem e responda.")

# Perguntas do quiz com imagens
perguntas = [
    {
        "pergunta": "Qual série da Netflix é essa imagem?",
        "imagem_url": "https://atlantidasc.com.br/wp-content/uploads/2025/07/Nova-temporada-de-Stranger-Things-deve-ser-a-conclusao-da-historia-Foto_-Netflix-Divulgacao.jpg",
        "alternativas": ["Dark", "Stranger Things", "Black Mirror", "The OA"],
        "resposta_certa": "Stranger Things"
    },
    {
        "pergunta": "Qual série é mostrada nesta imagem?",
        "imagem_url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgb9Zt5T1wPmEeOnb4ZRiPuccJiJ89HxBexhRwtHE_0Kqqp-2QY6HiNuqIc3usaBp9buuLJDSY9QVtP9Wa-odj8cAVppf3zKPGVwjc2WoPhXXOuxFGTFP3WFDa3rT93-hmymVqVxbjh2Bs0hkIzR3sE14FH2gt3WAe8PI_hKBaE_NO5DLXDJllldt-E_w/s1106/The_Witcher_Netflix_Termporada_3a.jpg",
        "alternativas": ["Vikings", "O Bruxo", "Game of Thrones", "Castlevania"],
        "resposta_certa": "O Bruxo"
    },
    {
        "pergunta": "Qual é essa série?",
        "imagem_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2024/09/episodio-USS-Callister-de-black-mirror.png?w=1024",
        "alternativas": ["Love, Death & Robots", "Black Mirror", "Westworld", "Black Summer"],
        "resposta_certa": "Black Mirror"
    },
    {
        "pergunta": "Que série é essa?",
        "imagem_url": "https://classic.exame.com/wp-content/uploads/2019/10/la-casa-de-papel-1.jpg",
        "alternativas": ["Elite", "La casa de papel", "Narcos", "Sky Rojo"],
        "resposta_certa": "La casa de papel"
    },
    {
        "pergunta": "E esta, qual é?",
        "imagem_url": "https://i.ytimg.com/vi/YPdAF6F4xIU/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCuCxb84spR_sfj5jF3eb2EZxBDSg",
        "alternativas": ["Alice in Borderland", "Round 6", "Lupin", "1899"],
        "resposta_certa": "Round 6"
    },
    {
        "pergunta": "Essa imagem representa qual série?",
        "imagem_url": "https://jpimg.com.br/uploads/2020/12/o-gambito-da-rainha-ofc-1024x664.jpg",
        "alternativas": ["House of Cards", "The Queen's Gambit", "Designated Survivor", "Ozark"],
        "resposta_certa": "The Queen's Gambit"
    },
    {
        "pergunta": "Que série é esta?",
        "imagem_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuD5sYqEe7L97PVGV6VPcg0PsXt9Z4Vvu9A&s",
        "alternativas": ["Outlander", "Bridgerton", "The Crown", "Downton Abbey"],
        "resposta_certa": "Bridgerton"
    },
    {
        "pergunta": "Qual é essa série/mídia?",
        "imagem_url": "https://s2-techtudo.glbimg.com/PBPfMFqS6FqcLaTJWaqZ0ZupLmw=/0x0:1044x562/888x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2023/P/R/rUKVWXSDypvwL1fwM49A/outer-banks-imdb-techtudo.jpg",
        "alternativas": ["Outer Banks", "The Mandalorian", "Lord of the Rings", "Cursed"],
        "resposta_certa": "Outer Banks"
    },
    {
        "pergunta": "Essa imagem é de qual título?",
        "imagem_url": "https://rollingstone.com.br/wp-content/uploads/sintonia-serie-brasileira-netflix-2-temporada-foto-divulgacao.jpg",
        "alternativas": ["Lost in Space", "Sintonia", "Dark", "Locke & Key"],
        "resposta_certa": "Sintonia"
    },
    {
        "pergunta": "Última – que anime é esse?",
        "imagem_url": "https://s2-techtudo.glbimg.com/HoMldM4KGCNWFh78XPF-Ogga0yY=/0x0:1380x825/888x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2024/r/A/MnpMb4R5egfC7H2AcktA/captura-de-tela-2024-10-27-141550.png",
        "alternativas": ["Haikyu", "Dandadan", "Naruto", "Jujutsu Kaisen"],
        "resposta_certa": "Dandadan"
    },
]

# Estado inicial
if "etapa" not in st.session_state:
    st.session_state.etapa = 0
    st.session_state.pontuacao = 0
    st.session_state.mostrando_resposta = False
    st.session_state.respostas_embaralhadas = []

etapa = st.session_state.etapa
pontuacao = st.session_state.pontuacao
mostrando_resposta = st.session_state.mostrando_resposta

# Fim do quiz
if etapa >= len(perguntas):
    st.success(f"🏁 Fim do Quiz! Sua pontuação final: {pontuacao} de {len(perguntas)}")
    if st.button("🔁 Recomeçar"):
        st.session_state.etapa = 0
        st.session_state.pontuacao = 0
        st.session_state.mostrando_resposta = False
        st.session_state.respostas_embaralhadas = []
        st.rerun()
    st.stop()

# Pergunta atual
pergunta_atual = perguntas[etapa]

# Embaralhar alternativas apenas uma vez por pergunta
if len(st.session_state.respostas_embaralhadas) <= etapa:
    alternativas_embaralhadas = random.sample(pergunta_atual["alternativas"], len(pergunta_atual["alternativas"]))
    st.session_state.respostas_embaralhadas.append(alternativas_embaralhadas)
else:
    alternativas_embaralhadas = st.session_state.respostas_embaralhadas[etapa]

# Exibição
st.subheader(f"Pergunta {etapa + 1} de {len(perguntas)}")
st.write(pergunta_atual["pergunta"])

# Imagem
response = requests.get(pergunta_atual["imagem_url"])
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    st.image(img, use_container_width=True)

# Alternativas
resposta_escolhida = st.radio("Escolha uma opção:", alternativas_embaralhadas, key=f"pergunta_{etapa}")

# Confirmação
if st.button("Confirmar resposta") and not mostrando_resposta:
    st.session_state.mostrando_resposta = True
    if resposta_escolhida == pergunta_atual["resposta_certa"]:
        st.success("✅ Resposta correta!")
        st.session_state.pontuacao += 1
    else:
        st.error(f"❌ Resposta errada! A correta era: **{pergunta_atual['resposta_certa']}**")

# Próxima
if mostrando_resposta:
    if st.button("Próxima"):
        st.session_state.etapa += 1
        st.session_state.mostrando_resposta = False
        st.rerun()
