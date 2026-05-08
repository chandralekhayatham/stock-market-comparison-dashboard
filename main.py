import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📈 Stock Market Comparison Dashboard")

st.write("Compare multiple stocks using real-time market data.")

# -----------------------------
# STOCK INPUT
# -----------------------------
stocks = st.text_input(
    "Enter Stock Symbols (comma separated)",
    "AAPL,TSLA,MSFT"
)

stock_list = [stock.strip().upper() for stock in stocks.split(",")]

# -----------------------------
# BUTTON
# -----------------------------
if st.button("Analyze Stocks"):

    close_df = pd.DataFrame()

    for stock in stock_list:

        data = yf.download(stock, period="6mo")

        if not data.empty:

            close_df[stock] = data["Close"]

    # -----------------------------
    # DISPLAY DATA
    # -----------------------------
    st.subheader("📊 Closing Prices")

    st.write(close_df.tail())

    # -----------------------------
    # PRICE COMPARISON CHART
    # -----------------------------
    st.subheader("📈 Stock Price Comparison")

    fig, ax = plt.subplots(figsize=(12,6))

    for stock in close_df.columns:
        ax.plot(close_df.index, close_df[stock], label=stock)

    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.legend()

    st.pyplot(fig)

    # -----------------------------
    # DAILY RETURNS
    # -----------------------------
    returns = close_df.pct_change()

    st.subheader("📉 Daily Returns")

    fig2, ax2 = plt.subplots(figsize=(12,6))

    for stock in returns.columns:
        ax2.plot(returns.index, returns[stock], label=stock)

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Daily Return")
    ax2.legend()

    st.pyplot(fig2)

    # -----------------------------
    # VOLATILITY
    # -----------------------------
    st.subheader("📌 Volatility Analysis")

    volatility = returns.std() * (252 ** 0.5)

    st.write(volatility)

    # -----------------------------
    # SAVE CSV
    # -----------------------------
    close_df.to_csv("stock_comparison.csv")

    st.success("Stock comparison report saved successfully ✅")