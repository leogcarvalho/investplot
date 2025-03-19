import streamlit as st
import plotly.express as px
from data import obter_dados_acao
import yfinance as yf

st.set_page_config(page_title="Análise de Ativos B3", layout="wide")

st.title("📈 Análise de Ativos B3")

# Criando uma variável no session_state para armazenar o ticker
if "ativo" not in st.session_state:
    st.session_state.ativo = None

# Input para selecionar o ativo
ticker = st.text_input("Digite o código do ativo (ex: PETR4)", "PETR4")

# Botão para buscar dados
if st.button("Buscar"):
    st.session_state.ativo = ticker  # Armazena o ticker no estado

# Se já há um ativo armazenado, processamos os dados
if st.session_state.ativo:
    with st.spinner("Carregando dados..."):
        indicadores, _ = obter_dados_acao(st.session_state.ativo)
        ticker_yf = yf.Ticker(f"{st.session_state.ativo.upper()}.SA")

        cotacao_atual = ticker_yf.history(period="1d")["Close"].iloc[-1]
        fechamento_anterior = ticker_yf.history(period="2d")["Close"].iloc[0]
        variacao = ((cotacao_atual - fechamento_anterior) / fechamento_anterior) * 100

        # 🌟 Seção 1: Informações Financeiras
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("💰 Cotação Atual")
            st.metric(label="Preço Agora", value=f"R$ {cotacao_atual:.2f}")
        with col2:
            st.subheader("📉 Fechamento do Dia Anterior")
            st.metric(label="Fechamento", value=f"R$ {fechamento_anterior:.2f}")
        with col3:
            st.subheader("📊 Variação do Dia")
            st.metric(label="Variação (%)", value=f"{variacao:.2f}%", delta=f"{variacao:.2f}%")

        # 🌟 Seção 2: Indicadores Fundamentais
        st.markdown("---")
        st.subheader("📊 Indicadores Fundamentais")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**📌 Nome:** <br> {indicadores['Nome']}", unsafe_allow_html=True)
            st.metric(label="🏢 Setor", value=indicadores["Setor"])
        with col2:
            st.metric(label="💹 P/L", value=f"{indicadores['P/L']:.2f}" if indicadores["P/L"] != "N/A" else "N/A")
            st.metric(label="📖 P/VPA", value=f"{indicadores['P/VPA']:.2f}" if indicadores["P/VPA"] != "N/A" else "N/A")
            dividend_yield = f"{indicadores['Dividend Yield (%)']:.2f}%" if indicadores["Dividend Yield (%)"] != "N/A" else "N/A"
            st.metric(label="💰 Dividend Yield (%)", value=dividend_yield)

        # 🌟 Seção 3: Gráfico de Histórico de Preços com Seletor de Período
        st.markdown("---")
        st.subheader("📈 Histórico de Preços")

        # Seletor de período
        periodos = {"1 Dia": "1d", "7 Dias": "7d", "30 Dias": "30d", "1 Ano": "1y", "5 Anos": "5y", "10 Anos": "10y"}
        periodo_selecionado = st.selectbox("Selecione o período", list(periodos.keys()), index=3)

        # Atualizar os dados do gráfico sem limpar a tela
        historico = ticker_yf.history(period=periodos[periodo_selecionado])
        fig = px.line(historico, x=historico.index, y="Close", title=f"Preço de {st.session_state.ativo.upper()} - {periodo_selecionado}")
        st.plotly_chart(fig)
