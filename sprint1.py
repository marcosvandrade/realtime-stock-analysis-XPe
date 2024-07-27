#!/usr/bin/env python
# coding: utf-8

# ### SPRINT 1

# #### Pesquisar APIs de dados financeiros

# Seguem abaixo as principais APIs para captura de dados financeiros:
#
# 1. Alpha Vantage:
#
# Oferece dados financeiros globais, incluindo ações, forex, criptomoedas e indicadores econômicos. Possui uma API gratuita com limites de uso.
#
# Biblioteca Python: alpha_vantage

# ##### exemplo de uso do Alpha Vantage

# In[ ]:


# from alpha_vantage.timeseries import TimeSeries

# ts = TimeSeries(key='sua_chave_api')
# data, meta_data = ts.get_intraday(symbol='PETR4.SA', interval='1min', outputsize='full')


# 2. IEX Cloud:
#
# Disponibiliza dados financeiros globais, com uma API gratuita e planos pagos para dados mais avançados.
#
# Biblioteca Python: iexfinance

# ##### exemplo de uso do IEX Cloud

# In[ ]:


# from iexfinance.stocks import Stock

# stock = Stock("AAPL", token="sua_chave_api")
# data = stock.get_quote()


# 3. Quandl:
#
# Oferece uma vasta gama de dados financeiros, incluindo ações, moedas, commodities e indicadores econômicos. Possui planos gratuitos e pagos.
#
# Biblioteca Python: quandl

# ##### exemplo de uso do Quandl

# In[ ]:


# import quandl

# quandl.ApiConfig.api_key = 'sua_chave_api'
# data = quandl.get("WIKI/GOOGL")


# 4. Yahoo Finance:
#
# Muito popular para dados históricos e atuais de ações, criptomoedas e outras informações financeiras.
#
# Biblioteca Python: yfinance

# ##### exemplo de uso do Yahoo Finance

# In[ ]:


# import yfinance as yf

# data = yf.download('PETR4.SA', start='2021-01-01', end='2021-12-31')


# 5. B3 API:
#
# A B3 (Bolsa de Valores do Brasil) oferece algumas APIs para acesso a dados financeiros. Embora algumas sejam pagas, há informações públicas disponíveis.
#
# Não possui uma biblioteca oficial em Python, mas você pode usar requests para fazer chamadas HTTP.

# ##### exemplo de uso do B3 API

# In[ ]:


# import requests

# url = "https://api.b3.com.br/data/endpoint"
# response = requests.get(url)
# data = response.json()


# 6. Investing.com:
#
# Oferece dados de mercado de vários países, incluindo o Brasil. Para acessar a API, geralmente é necessário web scraping.
#
# Biblioteca Python: investpy (mas verifique se ainda está funcionando, pois houve bloqueios recentes).

# ##### exemplo de uso do Investing.com

# In[ ]:


# import investpy

# data = investpy.get_stock_historical_data(stock='PETR4',
#                                          country='brazil',
#                                          from_date='01/01/2021',
#                                          to_date='31/12/2021')


# #### Configurar o ambiente para desenvolvimento e testes

# Para o ambiente de desenvolvimento optei por utilizar o sistema operacional Windows 11, para escrita do código utilizei o Visual Studio Code (VScode) com a extensão do Jupyter Notebook e do python como linguagem de programação, conforme imagens abaixo:

# Para controle de versão estou utilizando o git com Github gerenciado através de linha de comando com o Cmder conforme imagens abaixo:

# #### Configurar o ambiente para desenvolvimento e testes

# #### Para criação da interface do usuário utilizaremos o Framework python Streamlit

# In[1]:


# importando a biblioteca streamlit e atribuindo o apelido "st"
import streamlit as st  # type: ignore

# bliblioteca responsável pela atualização automática da página web
from streamlit_autorefresh import st_autorefresh  # type: ignore


# ##### Optei em utilizar o Yahoo Finance por sua flexibilidade e por ser gratuito, sendo uma excelente opção para criação do protótipo, na minha opinião.

# In[2]:


# importando a biblioteca do yahoo finance
import yfinance as yf


# In[3]:


# importando bibliotecas para uso de datas
from datetime import datetime, timedelta


# In[4]:


# importando blibliotecas para exibir gráficos para testes da apelido
import plotly.graph_objs as go


# ##### Criando o script inicial da aplicação e realizando testes

# In[5]:


# Lista de países e intervalos de tempo
countries = ["Brazil", "United States"]
intervals = ["1d", "1wk", "1mo"]  # d - dia wk - semana mo - mês


# In[6]:


# Criando o filtro para o usuário selecionar o intervalo de pesquisa desejado
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# In[7]:


# função de cache do streamlit para evitar redundância de dados
@st.cache_data()

# criando a função para consulta do usuário
def consultar_acao(stock, from_date, to_date, interval):
    return yf.download(
        stock, start=from_date, end=to_date, interval=interval, progress=False
    )


# In[8]:


# criando uma função para formatar a data
def format_date(dt, format="%Y-%m-%d"):
    return dt.strftime(format)


# In[10]:


# função que cria um grafo para teste de consulta e tempo de retorno
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


# In[11]:


# criando a barra lateral da página web com algumas ações pré-selecionadas
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Select country:", countries)
stocks = ["AAPL", "MSFT", "GOOGL"]  # Example stocks, replace with your stock list
stock_select = st.sidebar.selectbox("Select the stock:", stocks)
from_date = st.sidebar.date_input("Start Date:", start_date)
to_date = st.sidebar.date_input("End Date:", end_date)
interval_select = st.sidebar.selectbox("Select the range:", intervals)
carregar_dados = st.sidebar.checkbox("Load Data")

grafico_line = st.empty()
grafico_candle = st.empty()


# In[12]:


# Definindo título e cabeçalhos iniciais para a Home Page
st.title("Análise Gráfica de Ações em Tempo Real")
st.header("Ações")
st.subheader("Análise Gráfica")


# In[13]:


# função para definir o tempo de atualização da página que visa permitir
# a análise em tempo real
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

if from_date > to_date:
    st.sidebar.error("Start Date greater than End Date")
else:
    df = consultar_acao(
        stock_select, format_date(from_date), format_date(to_date), interval_select
    )
    try:
        fig = plotCandleStick(df)
        grafico_candle.plotly_chart(fig)
        grafico_line.line_chart(df["Close"])
        if carregar_dados:
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(e)


# ##### Criaremos agora o servidor local do streamlit

# In[ ]:


# Para converter um script de Jupyter Notebook (.ipynb) para um script Python
# (.py), utilizaremos a ferramenta nbconvert que faz parte do Jupyter.

# utilizaremos o gerenciador de pacotes "pip" para instalação do jupyter
# get_ipython().system('pip install jupyter')


# In[14]:


# convertendo o script do jupyter notebook para python
# jupyter nbconvert --to script sprint1.ipynb


# ###### Para isso deveremos utilizar o comando # sreamlit run sprint1.py no terminal
