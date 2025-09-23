import streamlit as st
import requests
from datetime import datetime

# ==============================
# Configurações da API
# ==============================
API_KEY = "T8K3C6h5cA8kbKkC21zXpxDI7yJpnV5d"  # Chave fixa no código
BASE_URL = "https://api.nytimes.com/svc/topstories/v2"

# ==============================
# Logo e Cabeçalho
# ==============================
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/4/40/New_York_Times_logo_variation.jpg",
    width=200
)

st.title("📰 Principais Notícias do New York Times")

st.markdown("""
Esta aplicação consome a **API gratuita do New York Times** para exibir as principais histórias do dia.  
A API fornece artigos jornalísticos em JSON, incluindo título, resumo, autor e imagens.

**Seções disponíveis:** Home, Arts, Business, Politics, Sports, Technology.

📌 Documentação oficial: [developer.nytimes.com](https://developer.nytimes.com/docs/top-stories-product/1/overview)
""")

# ==============================
# Seleção de Seção
# ==============================
sections = ["home", "arts", "business", "politics", "sports", "technology"]
selected_section = st.selectbox("Escolha uma seção de notícias:", sections)

sections_descriptions = {
    "home": "📰 Notícias gerais e destaques da atualidade.",
    "arts": "🎭 Cobertura de artes, cultura e entretenimento.",
    "business": "💼 Notícias sobre negócios, economia e mercado.",
    "politics": "🏛️ Atualizações e análises do cenário político.",
    "sports": "⚽ Notícias e resultados esportivos.",
    "technology": "💻 Inovações e tendências do mundo tecnológico."
}

st.markdown(f"**{sections_descriptions[selected_section]}**")

# ==============================
# Função para pegar notícias
# ==============================
def get_news(section):
    url = f"{BASE_URL}/{section}.json?api-key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        st.error("Erro ao acessar a API do NYTimes!")
        return []

# ==============================
# Exibindo as notícias
# ==============================
articles = get_news(selected_section)

for article in articles[:10]:  # Mostra apenas as 10 primeiras
    title = article.get("title", "Sem título")
    abstract = article.get("abstract", "")
    byline = article.get("byline", "")
    url = article.get("url", "")
    image_url = ""

    # Pegar a primeira imagem se existir
    if article.get("multimedia"):
        image_url = article["multimedia"][0]["url"]

    # Exibir notícia como um card simples
    st.markdown("---")
    if image_url:
        st.image(image_url, width='stretch')  # Atualizado aqui
    st.markdown(f"### {title}")
    st.markdown(f"*{byline}*")
    st.markdown(abstract)
    st.markdown(f"[Leia mais]({url})")
