import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh

# List of stocks and intervals
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
intervals = ["1d", "1wk", "1mo"]

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# Function to get stock data
def consultar_acao(stock, start_date, end_date, interval):
    return yf.download(stock, start=start_date, end=end_date, interval=interval)


# Function to plot candlestick chart
def plotCandleStick(df, stock="stock"):
    trace1 = {
        "x": df.index,
        "open": df["Open"],
        "close": df["Close"],
        "high": df["High"],
        "low": df["Low"],
        "type": "candlestick",
        "name": stock,
        "showlegend": False,
    }

    data = [trace1]
    layout = go.Layout()

    return go.Figure(data=data, layout=layout)


# Creating the sidebar
st.sidebar.header("Stock Monitor")
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
    st.sidebar.error("Start date cannot be after end date")
else:
    df = consultar_acao(stock_select, from_date, to_date, interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df["Close"])
        if carregar_dados:
            st.subheader("Data")
            dados = st.dataframe(df)
    except Exception as e:
        st.error(e)
