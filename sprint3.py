#!/usr/bin/env python
# coding: utf-8

# #### SPRINT 3

# ##### ETAPA 1 DO TRELLO - MELHORANDO A INTERFACE GRÁFICA

# In[6]:


# importando a biblioteca do yahoo finance
import yfinance as yf

# importando a biblioteca streamlit e atribuindo o apelido "st"
import streamlit as st

# bliblioteca responsável pela atualização automática da página web
from streamlit_autorefresh import st_autorefresh

# importando blibliotecas para exibir gráficos
import plotly.graph_objs as go

# importando bibliotecas para uso de datas
from datetime import datetime, timedelta

# Criando uma lista de países e intervalos de tempo
countries = ["Brazil", "United States"]
intervals = ["1d", "1wk", "1mo"]


# criando uma função para formatar a data
def format_date(dt, format="%Y-%m-%d"):
    return dt.strftime(format)


# função de cache do streamlit para evitar redundância de dados
@st.cache_data()

# criando a função para consulta do usuário
def consultar_acao(stock, from_date, to_date, interval):
    return yf.download(
        stock, start=from_date, end=to_date, interval=interval, progress=False
    )


# criando uma função para formatar a data
def format_date(dt, format="%Y-%m-%d"):
    return dt.strftime(format)


# Criando o filtro para o usuário selecionar o intervalo de pesquisa desejado
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# função para exiblição dos gráficos
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


# criando a barra lateral da página web com algumas ações pré-selecionadas
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Escolha o país:", countries)
stocks = ["AAPL", "MSFT", "GOOGL"]
stock_select = st.sidebar.selectbox("Selecione a ação:", stocks)
from_date = st.sidebar.date_input("Data Inicial:", start_date)
to_date = st.sidebar.date_input("Data Final:", end_date)
interval_select = st.sidebar.selectbox(
    "Escolha o intervado de tempo desejado (d - dia wk - semana mo - mês):", intervals
)
carregar_dados = st.sidebar.checkbox("Carregar Dados")

grafico_line = st.empty()
grafico_candle = st.empty()


# In[3]:


# Definindo título e cabeçalhos para a Home Page
st.title("Análise Gráfica de Ações em Tempo Real")
st.header("Ações")
st.subheader("Análise Gráfica")


# In[4]:


# função para definir o tempo de atualização da página que visa permitir
# a análise em tempo real
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

# if count == 0:
#     st.write("Count is zero")
# elif count % 3 == 0 and count % 5 == 0:
#     st.write("FizzBuzz")
# elif count % 3 == 0:
#     st.write("Fizz")
# elif count % 5 == 0:
#     st.write("Buzz")
# else:
#     st.write(f"Count: {count}")

if from_date > to_date:
    st.sidebar.error("A data inicial deve ser menor que a data final")
else:
    df = consultar_acao(
        stock_select, format_date(from_date), format_date(to_date), interval_select
    )
    try:
        fig = plotCandleStick(df)
        grafico_candle.plotly_chart(fig)
        # grafico_line.line_chart(df["Close"])
        if carregar_dados:
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(e)
