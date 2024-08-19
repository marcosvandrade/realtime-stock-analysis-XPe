#!/usr/bin/env python
# coding: utf-8

# #### SPRINT 3

# ##### ETAPA 1 DO TRELLO - MELHORANDO A INTERFACE GRÁFICA

# In[6]:


# Importando as bibliotecas necessárias
import yfinance as yf
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Criando listas de países, principais ações e intervalos de tempo
countries = ["Brazil", "United States"]
intervals = ["1d", "1wk", "1mo"]

brazil_stocks = [
    "ABEV3.SA",
    "B3SA3.SA",
    "BBAS3.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BBSE3.SA",
    "BEEF3.SA",
    "BRAP4.SA",
    "BRFS3.SA",
    "BRKM5.SA",
    "BRML3.SA",
    "BTOW3.SA",
    "CCRO3.SA",
    "CIEL3.SA",
    "CMIG4.SA",
    "COGN3.SA",
    "CPFE3.SA",
    "CPLE6.SA",
    "CSAN3.SA",
    "CSNA3.SA",
    "CVCB3.SA",
    "CYRE3.SA",
    "ECOR3.SA",
    "EGIE3.SA",
    "ELET3.SA",
    "ELET6.SA",
    "EMBR3.SA",
    "ENBR3.SA",
    "ENGI11.SA",
    "EQTL3.SA",
    "EZTC3.SA",
    "FLRY3.SA",
    "GGBR4.SA",
    "GOAU4.SA",
    "GOLL4.SA",
    "HAPV3.SA",
    "HGTX3.SA",
    "HYPE3.SA",
    "IGTA3.SA",
    "IRBR3.SA",
    "ITSA4.SA",
    "ITUB4.SA",
    "JBSS3.SA",
    "KLBN11.SA",
    "LAME4.SA",
    "LIGT3.SA",
    "LINX3.SA",
    "LREN3.SA",
    "MGLU3.SA",
    "MRFG3.SA",
    "MRVE3.SA",
    "MULT3.SA",
    "NTCO3.SA",
    "PCAR3.SA",
    "PETR3.SA",
    "PETR4.SA",
    "QUAL3.SA",
    "RADL3.SA",
    "RAIL3.SA",
    "RENT3.SA",
    "SANB11.SA",
    "SBSP3.SA",
    "SULA11.SA",
    "SUZB3.SA",
    "TAEE11.SA",
    "TIMP3.SA",
    "TOTS3.SA",
    "UGPA3.SA",
    "USIM5.SA",
    "VALE3.SA",
    "VIVT3.SA",
    "VVAR3.SA",
    "WEGE3.SA",
    "YDUQ3.SA",
]

us_stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "FB",
    "TSLA",
    "NVDA",
    "AMD",
    "NFLX",
    "BABA",
    "PYPL",
    "INTC",
    "CSCO",
    "ADBE",
    "CMCSA",
    "PFE",
    "JNJ",
    "MRNA",
    "BA",
    "DIS",
    "T",
    "VZ",
    "WMT",
    "XOM",
    "CVX",
    "PG",
    "KO",
    "PEP",
    "MCD",
    "NKE",
    "V",
    "MA",
    "JPM",
    "BAC",
    "C",
    "GS",
    "MS",
    "AMGN",
    "GILD",
    "CRM",
    "SQ",
    "UBER",
    "LYFT",
    "SPCE",
    "NKLA",
    "PLTR",
    "SNOW",
    "NIO",
    "XPEV",
    "LI",
    "ARKK",
    "SPY",
    "QQQ",
    "DIA",
    "IWM",
    "GME",
    "AMC",
    "BB",
    "NOK",
    "TLRY",
    "CGC",
    "ACB",
    "ZNGA",
    "SIRI",
    "EBAY",
    "TWTR",
    "ROKU",
    "PINS",
    "UBER",
    "LYFT",
]

# Criando um dicionário para associar a lista de ações ao país selecionado
stock_options = {"United States": us_stocks, "Brazil": brazil_stocks}


# Função de cache do Streamlit para evitar redundância de dados
@st.cache_data()
def consultar_acao(stock, from_date, to_date, interval):
    return yf.download(
        stock, start=from_date, end=to_date, interval=interval, progress=False
    )


# Função para exibição dos gráficos
def plotCandleStick(df, acao="ticket"):
    trace1 = {
        "x": df.index,
        "open": df["Open"],
        "close": df["Close"],
        "high": df["High"],
        "low": df["Low"],
        "type": "candlestick",
        "name": acao,
        "showlegend": False,
    }
    data = [trace1]
    layout = go.Layout()
    return go.Figure(data=data, layout=layout)


# ##### Aplicando melhorias na barra lateral

# In[7]:


# Aplicando melhorias na barra lateral
barra_lateral = st.sidebar.empty()

# Atualizando a barra lateral para listar as ações de acordo com o país selecionado
country_select = st.sidebar.selectbox("Escolha o país:", countries)
stocks = stock_options[country_select]  # Obtém as ações do país selecionado
stock_select = st.sidebar.selectbox("Selecione a ação:", stocks)

# Criando o filtro para o usuário selecionar o intervalo de pesquisa desejado
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

from_date = st.sidebar.date_input("Data Inicial:", start_date.date())
to_date = st.sidebar.date_input("Data Final:", end_date.date())

# Formata as datas no formato brasileiro (DD/MM/YYYY) apenas para exibição
formatted_start_date = from_date.strftime("%d/%m/%Y")
formatted_end_date = to_date.strftime("%d/%m/%Y")
st.write(f"Data Inicial: {formatted_start_date}")
st.write(f"Data Final: {formatted_end_date}")

# Criando o restante da barra lateral
interval_select = st.sidebar.selectbox(
    "Escolha o intervalo de tempo desejado (d - dia wk - semana mo - mês):", intervals
)
carregar_dados = st.sidebar.checkbox("Carregar Dados")


# In[3]:


# Exibindo o título com tamanho de fonte personalizado
st.markdown(
    "<h1 style='font-size: 24px;'>Análise Gráfica de Ações em Tempo Real</h1>",
    unsafe_allow_html=True,
)


# In[4]:


# Função para definir o tempo de atualização da página que visa permitir a análise em tempo real
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

# Verificação de datas e exibição de gráficos
if from_date > to_date:
    st.sidebar.error("A data inicial deve ser menor que a data final")
else:
    df = consultar_acao(
        stock_select,
        from_date.strftime("%Y-%m-%d"),
        to_date.strftime("%Y-%m-%d"),
        interval_select,
    )

    try:
        fig = plotCandleStick(df)
        grafico_candle = st.empty()
        grafico_candle.plotly_chart(fig)

        if carregar_dados:
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(e)
S
