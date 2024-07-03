import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh
import time

# List of countries and intervals
countries = ["Brazil", "United States"]
intervals = ["Daily", "Weekly", "Monthly"]

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# Caching functions to avoid redundant data fetching
@st.cache_data
def consultar_acao(stock, country, from_date, to_date, interval):
    for _ in range(3):  # Retry mechanism
        try:
            df = ip.get_stock_historical_data(
                stock=stock,
                country=country,
                from_date=from_date,
                to_date=to_date,
                interval=interval,
            )
            return df
        except Exception as e:
            if "403" in str(e):
                st.warning("Request blocked. Retrying...")
                time.sleep(5)  # Wait before retrying
            else:
                raise e
    st.error("Failed to fetch data after several attempts.")
    return None


# Formatting date
def format_date(dt, format="%d/%m/%Y"):
    return dt.strftime(format)


# Plotting candlestick chart
def plotCandleStick(df, acao="ticket"):
    trace1 = {
        "x": df.index,
        "open": df.Open,
        "close": df.Close,
        "high": df.High,
        "low": df.Low,
        "type": "candlestick",
        "name": acao,
        "showlegend": False,
    }

    data = [trace1]
    layout = go.Layout()

    return go.Figure(data=data, layout=layout)


# Creating the sidebar
country_select = st.sidebar.selectbox("Select country:", countries)
stocks = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Select the stock:", stocks)
from_date = st.sidebar.date_input("Start Date:", start_date)
to_date = st.sidebar.date_input("End Date:", end_date)
interval_select = st.sidebar.selectbox("Select the range:", intervals)
carregar_dados = st.sidebar.checkbox("Load Data")

# Central page elements
st.title("Graphical Analysis of Stocks in Real-Time")
st.header("Stocks")
st.subheader("Graphical Analysis")

# Auto-refresh functionality
# count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

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

# Load data and plot if the date range is valid
if from_date > to_date:
    st.sidebar.error("Start date must be before end date.")
elif carregar_dados:
    try:
        df = consultar_acao(
            stock_select,
            country_select,
            format_date(from_date),
            format_date(to_date),
            interval_select,
        )
        if df is not None:
            fig = plotCandleStick(df)
            st.plotly_chart(fig)
            st.line_chart(df["Close"])
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
