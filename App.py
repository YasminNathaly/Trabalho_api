import streamlit as st
import requests
import pandas as pd

# Substitua pela sua chave da API do New York Times
API_KEY = "T8K3C6h5cA8kbKkC21zXpxDI7yJpnV5d"

# Função para buscar artigos usando a API Search do NYT
def search_articles(query, page=0):
    """
    Busca artigos no NYT usando a API Search.
    Parâmetros:
        query (str): termo de busca
        page (int): página de resultados (0 a 100)
    Retorna:
        dict: resposta JSON da API ou None em caso de erro
    """
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": query,
        "api-key": API_KEY,
        "page": page,
        "sort": "relevance"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
        return None

# Função para extrair dados relevantes dos artigos
def parse_articles(data):
    """
    Extrai informações relevantes dos artigos retornados pela API.
    Parâmetros:
        data (dict): JSON retornado pela API
    Retorna:
        pd.DataFrame: DataFrame com colunas Título, Autor, Data, Resumo, URL
    """
    docs = data.get("response", {}).get("docs", [])
    articles = []
    for doc in docs:
        headline = doc.get("headline", {}).get("main", "Sem título")
        snippet = doc.get("snippet", "")
        pub_date = doc.get("pub_date", "")[:10]  # formato YYYY-MM-DD
        web_url = doc.get("web_url", "")
        byline = doc.get("byline", {}).get("original", "Autor não informado")
        articles.append({
            "Título": headline,
            "Resumo": snippet,
            "Autor": byline,
            "Data": pub_date,
            "URL": web_url
        })
    return pd.DataFrame(articles)

# Configurações da página Streamlit
st.set_page_config(page_title="Busca NYT", layout="wide")

# Título e descrição
st.title("🔎 Busca de Artigos no New York Times")
st.markdown("""
Esta aplicação permite pesquisar artigos do New York Times por palavra-chave.
Você pode navegar entre páginas de resultados e acessar os links das matérias originais.
""")

# Input para termo de busca
query = st.text_input("Digite o termo para pesquisa:", "")

# Controle de página para paginação
if "page" not in st.session_state:
    st.session_state.page = 0

# Botões para navegação entre páginas
def next_page():
    st.session_state.page += 1

def prev_page():
    if st.session_state.page > 0:
        st.session_state.page -= 1

# Quando o usuário digita um termo
if query:
    with st.spinner("Buscando artigos..."):
        data = search_articles(query, st.session_state.page)

    if data:
        df = parse_articles(data)
        if not df.empty:
            st.markdown(f"### Resultados para: '{query}' (Página {st.session_state.page + 1})")
            
            # Mostrar artigos com links clicáveis
            for idx, row in df.iterrows():
                st.markdown(f"**{row['Título']}**")
                st.markdown(f"*{row['Autor']}* - {row['Data']}")
                st.markdown(f"{row['Resumo']}")
                st.markdown(f"[Leia a matéria completa aqui]({row['URL']})")
                st.markdown("---")

            # Navegação entre páginas
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.session_state.page > 0:
                    st.button("⬅️ Página Anterior", on_click=prev_page)
            with col3:
                # A API permite até 100 páginas (0 a 99)
                if st.session_state.page < 99:
                    st.button("Próxima Página ➡️", on_click=next_page)
        else:
            st.warning("Nenhum artigo encontrado para este termo.")
else:
    st.info("Digite um termo acima para iniciar a busca.")
