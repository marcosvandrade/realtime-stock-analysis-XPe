import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh

# List of countries and intervals
countries = ["Brazil", "United States"]
intervals = ["1d", "1wk", "1mo"]  # Adjusting intervals for yfinance

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# Caching functions to avoid redundant data fetching
@st.cache_data()
def consultar_acao(stock, from_date, to_date, interval):
    return yf.download(stock, start=from_date, end=to_date, interval=interval, progress=False)

# Formatting date
def format_date(dt, format="%Y-%m-%d"):
    return dt.strftime(format)

# Plotting candlestick chart
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

# Creating the sidebar
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

# Central page elements
st.title("Graphical Analysis of Stocks in Real-Time")
st.header("Stocks")
st.subheader("Graphical Analysis")

# Auto-refresh functionality
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
    df = consultar_acao(stock_select, format_date(from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle.plotly_chart(fig)
        grafico_line.line_chart(df["Close"])
        if carregar_dados:
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(e)
